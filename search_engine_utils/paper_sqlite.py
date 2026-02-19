"""
SQLite database manager for paper data.

Provides functionality to create and query a SQLite database from paper summaries.
"""
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
from loguru import logger

from .search_utils import fuzzy_match


# Database schema definition
DB_SCHEMA = {
    "table_name": "papers",
    "columns": [
        {
            "name": "title",
            "type": "TEXT",
            "description": "paper title"
        },
        {
            "name": "published_at",
            "type": "TEXT",
            "description": "publication date in YYYY-MM-DD format"
        },
        {
            "name": "url",
            "type": "TEXT",
            "description": "arXiv link to the paper"
        },
        {
            "name": "content",
            "type": "TEXT",
            "description": "paper summary/abstract"
        },
        {
            "name": "date_added",
            "type": "TEXT",
            "description": "the date when the paper was added to our database"
        },
        {
            "name": "personal_notes",
            "type": "TEXT",
            "description": "personal notes written by Xin (from dailies/notes/{date_added}.md)"
        }
    ]
}


class PaperSqliteManager:
    """Manager for SQLite database of paper summaries."""

    def __init__(
        self,
        paper_summaries_path: Path,
        sqlite_path: Path,
        overwrite: bool = False
    ):
        """
        Initialize the SQLite manager.

        Args:
            paper_summaries_path: Path to summaries.jsonl file
            sqlite_path: Path where SQLite database should be created/loaded
            overwrite: If True, recreate the database from scratch
        """
        self.paper_summaries_path = paper_summaries_path
        self.sqlite_path = sqlite_path

        if overwrite or not sqlite_path.exists():
            self.create_database()
        else:
            logger.info(f"Using existing SQLite database at {sqlite_path}")

    def create_database(self):
        """Create SQLite database from summaries.jsonl file."""
        logger.info(f"Creating SQLite database at {self.sqlite_path}")

        # Use dict to deduplicate by title, keeping the latest entry
        papers_dict = {}
        with self.paper_summaries_path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    paper_data = json.loads(line)
                    title = paper_data.get('title')
                    if title:  # Only add if title exists
                        papers_dict[title] = paper_data

        # Convert dict back to list
        all_paper_data = list(papers_dict.values())
        logger.info(f"Loaded {len(all_paper_data)} unique papers")

        conn = sqlite3.connect(str(self.sqlite_path))
        cur = conn.cursor()

        # Drop existing table to ensure clean state
        cur.execute("DROP TABLE IF EXISTS papers")

        # Create table
        cur.execute("""
        CREATE TABLE papers (
            title TEXT PRIMARY KEY,
            published_at TEXT,
            url TEXT,
            content TEXT,
            date_added TEXT,
            personal_notes TEXT
        )
        """)

        conn.commit()

        # Insert data
        insert_sql = """
        INSERT OR REPLACE INTO papers (
            title, published_at, url, content, date_added, personal_notes
        ) VALUES (?, ?, ?, ?, ?, ?)
        """

        for paper in all_paper_data:
            # Get date_added from 'date' field
            date_added = paper.get("date")

            # Load personal notes if available
            personal_notes = None
            if date_added:
                notes_file = Path('dailies') / 'notes' / f'{date_added}.md'
                if notes_file.exists():
                    try:
                        with open(notes_file, 'r', encoding='utf-8') as f:
                            personal_notes = f.read().strip()
                    except Exception as e:
                        logger.warning(f"Failed to load notes for {date_added}: {e}")

            cur.execute(
                insert_sql,
                (
                    paper.get("title"),
                    paper.get("published_at"),
                    paper.get("url"),
                    paper.get("content"),
                    date_added,
                    personal_notes,
                )
            )

        conn.commit()
        conn.close()
        logger.info(f"Database created successfully with {len(all_paper_data)} papers")

    def _register_udfs(self, conn: sqlite3.Connection):
        """
        Register custom SQL functions for paper queries.

        Args:
            conn: SQLite connection
        """
        # Register the fuzzy_match function from search_utils
        conn.create_function(name="fuzzy_match", narg=2, func=fuzzy_match)

    def query_df(self, sql: str) -> pd.DataFrame:
        """
        Execute SQL query and return results as pandas DataFrame.

        Args:
            sql: SQL query string

        Returns:
            DataFrame with query results
        """
        with sqlite3.connect(str(self.sqlite_path)) as conn:
            # Register any custom UDFs
            self._register_udfs(conn)
            return pd.read_sql_query(sql, conn)

    def query_dict(self, sql: str) -> List[Dict[str, Any]]:
        """
        Execute SQL query and return results as list of dictionaries.

        Args:
            sql: SQL query string

        Returns:
            List of dictionaries, one per row
        """
        df = self.query_df(sql)
        return df.to_dict(orient="records")

    @staticmethod
    def get_schema() -> Dict[str, Any]:
        """
        Get database schema information.

        Returns:
            Dictionary with table name and column definitions
        """
        return DB_SCHEMA

    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Dictionary with database statistics
        """
        with sqlite3.connect(str(self.sqlite_path)) as conn:
            cur = conn.cursor()

            # Get total count
            cur.execute("SELECT COUNT(*) FROM papers")
            total_count = cur.fetchone()[0]

            # Get date range
            cur.execute("""
                SELECT
                    MIN(published_at) as earliest,
                    MAX(published_at) as latest
                FROM papers
                WHERE published_at IS NOT NULL
            """)
            date_range = cur.fetchone()

            return {
                "total_papers": total_count,
                "earliest_paper": date_range[0],
                "latest_paper": date_range[1],
                "database_path": str(self.sqlite_path)
            }
