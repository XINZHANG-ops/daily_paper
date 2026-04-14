#!/usr/bin/env python3
"""
Test script for search endpoints.

Tests both FAISS vector search and wiki-based Q&A.
"""
import requests
import json

API_URL = "http://localhost:5001"

def test_vector_search():
    """Test FAISS hybrid search endpoint."""
    print("\n" + "="*60)
    print("TEST 1: FAISS Vector Search")
    print("="*60)

    response = requests.post(
        f"{API_URL}/search",
        json={
            "query": "agent systems and autonomous agents",
            "k": 3,
            "return_scores": True
        }
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['num_results']} results\n")

        for i, result in enumerate(data['results'][:3], 1):
            print(f"Result {i}:")
            print(f"  Score: {result.get('score', 'N/A'):.3f}")
            print(f"  Title: {result['metadata'].get('title', 'N/A')[:60]}")
            print(f"  Content: {result['content'][:150]}...")
            print()
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)


def test_sql_query():
    """Test SQLite query endpoint."""
    print("\n" + "="*60)
    print("TEST 2: SQL Query")
    print("="*60)

    response = requests.post(
        f"{API_URL}/query",
        json={
            "sql": "SELECT title, date_added FROM papers ORDER BY date_added DESC LIMIT 5"
        }
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Found {data['num_results']} papers\n")

        for paper in data['results']:
            print(f"  {paper['date_added']}: {paper['title'][:60]}")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)


def test_wiki_qa():
    """Test wiki-based Q&A endpoint."""
    print("\n" + "="*60)
    print("TEST 3: Wiki Q&A")
    print("="*60)

    print("Sending question to agent (may take 30-60 seconds)...\n")

    response = requests.post(
        f"{API_URL}/ask_wiki",
        json={
            "question": "总结一下 agent systems 这个主题，有哪些代表性论文？",
            "model": "minimax-m2.7:cloud"
        },
        timeout=120  # 2 minutes timeout
    )

    if response.status_code == 200:
        data = response.json()
        print("✓ Answer received:\n")
        print(data['answer'])
        print(f"\n(Model: {data['model']})")
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)


def main():
    print("Testing daily_paper search endpoints...")
    print(f"API URL: {API_URL}")

    try:
        # Test 1: FAISS search
        test_vector_search()

        # Test 2: SQL query
        test_sql_query()

        # Test 3: Wiki Q&A (slowest, using agent)
        test_wiki_qa()

        print("\n" + "="*60)
        print("All tests completed!")
        print("="*60)

    except requests.exceptions.ConnectionError:
        print(f"\n✗ Error: Could not connect to {API_URL}")
        print("Make sure serve_search.py is running on port 5001")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
