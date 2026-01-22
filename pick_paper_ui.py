"""
Gradio UI for selecting daily papers - ONE AT A TIME VERSION

Process papers one at a time with full visibility and control.
"""

import os
import sys
import json
import gradio as gr
import threading
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from loguru import logger
from typing import List, Dict
from queue import Queue, Empty

# Import existing utilities
from utils.huggingface_utils import fetch_huggingface_papers, process_papers
from utils.file_utils import find_not_proposed_papers
from utils.ai_utils import process_paper
from daily_papers import create_subpage, update_index_page
from utils.google_chat_utils import start_thread, send_articles


def push_to_github():
    """Push changes to GitHub repository."""
    import subprocess
    subprocess.run(["git", "add", "index.html", "dailies/pages/", "dailies/notes/", "dailies/images/"])
    subprocess.run(["git", "add", "summaries.jsonl"])
    subprocess.run(["git", "commit", "-m", "Daily Paper Push"])
    subprocess.run(["git", "push", "origin", "main"])


def get_arxiv_abstract(arxiv_id: str) -> str:
    """Get abstract from arXiv API."""
    try:
        api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entry = root.find('.//atom:entry', ns)
            if entry:
                abstract = entry.find('.//atom:summary', ns)
                if abstract is not None:
                    text = abstract.text.strip()
                    text = ' '.join(text.split())
                    if len(text) > 150:
                        text = text[:150] + "..."
                    return text
    except Exception as e:
        logger.error(f"Error fetching abstract for {arxiv_id}: {e}")
    return "Abstract not available"


# Global state
all_papers = []
processed_papers = []  # Successfully processed papers
processing_log = []  # Log of processing attempts
processing_thread = None


def get_log_text():
    """Get current log as formatted text."""
    if not processing_log:
        return "Click 'Load Papers' to start..."
    return "\n".join(processing_log)


def add_log(message):
    """Add a message to the processing log."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    processing_log.append(f"[{timestamp}] {message}")
    logger.info(message)


def load_papers():
    """Load papers from HuggingFace."""
    global all_papers, processed_papers, processing_log

    # Reset state
    processed_papers = []
    processing_log = []

    add_log("🔄 Loading papers from HuggingFace...")

    # Fetch and process papers
    papers = fetch_huggingface_papers(100)
    processed = process_papers(papers, 'hot')

    # Filter out seen papers
    current_paper_titles = []
    try:
        with open('summaries.jsonl', 'r', encoding='utf-8') as file:
            for line in file:
                summary = json.loads(line.strip())
                current_paper_titles.append(summary['title'])
    except FileNotFoundError:
        add_log("⚠️ summaries.jsonl not found")

    unseen_papers, _ = find_not_proposed_papers(processed, current_paper_titles)

    # Add abstracts and arXiv links to first 30 papers
    for paper in unseen_papers[:30]:
        import re
        match = re.search(r'(\d{4}\.\d+)', paper.get('paper_id', ''))
        if match:
            arxiv_id = match.group(1)
            paper['abstract'] = get_arxiv_abstract(arxiv_id)
            paper['arxiv_url'] = f"https://arxiv.org/abs/{arxiv_id}"
        else:
            paper['abstract'] = "N/A"
            paper['arxiv_url'] = "#"

    all_papers = unseen_papers[:30]
    add_log(f"✅ Loaded {len(all_papers)} unseen papers")

    # Create choices for radio button
    choices = []
    for i, paper in enumerate(all_papers):
        label = f"{i+1}. {paper['title'][:80]}... ({paper.get('published_at', 'Unknown')[:10]})"
        choices.append(label)

    return (
        gr.update(choices=choices, value=None),
        get_log_text(),
        gr.update(visible=False),  # Hide finish button
        ""  # Clear paper preview
    )


def show_paper_preview(selected_choice):
    """Show preview of selected paper with arXiv link."""
    if not selected_choice or not all_papers:
        return ""

    # Extract index
    idx = int(selected_choice.split('.')[0]) - 1
    if idx >= len(all_papers):
        return ""

    paper = all_papers[idx]

    # Format preview with markdown
    preview = f"""
### {paper['title']}

**Published:** {paper.get('published_at', 'Unknown')[:10]}

**Abstract:** {paper.get('abstract', 'N/A')}

**arXiv Link:** [View on arXiv]({paper.get('arxiv_url', '#')})
"""
    return preview


def process_single_paper(selected_choice, model_name):
    """Process one selected paper."""
    global processing_thread, all_papers, processed_papers

    if not selected_choice:
        add_log("❌ Please select a paper first!")
        return get_log_text(), gr.update(visible=False)

    # Check if already processing
    if processing_thread and processing_thread.is_alive():
        add_log("⚠️ Already processing a paper, please wait!")
        return get_log_text(), gr.update(visible=False)

    # Extract index
    idx = int(selected_choice.split('.')[0]) - 1
    if idx >= len(all_papers):
        add_log("❌ Invalid paper selection!")
        return get_log_text(), gr.update(visible=False)

    paper = all_papers[idx]
    paper_title = paper['title'][:50] + "..."

    add_log(f"🔄 Processing: {paper_title}")

    # Process in background
    def process():
        result_queue = Queue()
        thread = threading.Thread(
            target=process_paper,
            args=(paper, result_queue, 24000, model_name)
        )
        thread.start()
        thread.join(timeout=150)

        if not thread.is_alive():
            try:
                result = result_queue.get_nowait()
                if result and not isinstance(result, str):
                    paper_info, _ = result
                    processed_papers.append(paper_info)
                    add_log(f"✅ SUCCESS: {paper_title}")
                    add_log(f"📊 Progress: {len(processed_papers)} papers completed")
                else:
                    add_log(f"❌ FAILED: {paper_title} - {result if isinstance(result, str) else 'Unknown error'}")
            except Empty:
                add_log(f"❌ FAILED: {paper_title} - No result returned")
        else:
            add_log(f"⏱️ TIMEOUT: {paper_title} - Took too long")

    processing_thread = threading.Thread(target=process)
    processing_thread.start()

    # Wait for completion and return updated log
    processing_thread.join()

    return get_log_text(), gr.update(visible=False)


def finish_and_send(daily_total):
    """Finish processing and send to GitHub/Google Chat."""
    global processed_papers

    if len(processed_papers) < daily_total:
        add_log(f"❌ Only {len(processed_papers)}/{daily_total} papers processed!")
        return get_log_text()

    add_log("🚀 Finalizing and sending...")

    # Take only the required number of papers
    articles = processed_papers[:daily_total]

    TEST = os.getenv('TEST', 'FALSE')
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Save to summaries.jsonl
    if TEST == 'FALSE':
        add_log("💾 Saving to summaries.jsonl...")
        with open('summaries.jsonl', 'a') as f:
            for paper_info in articles:
                paper_info['date'] = current_date
                f.write(json.dumps(paper_info) + '\n')

    # Get quote (matching daily_papers.py logic)
    add_log("📝 Getting inspirational quote...")
    import uuid
    import time
    from inspirational_quotes import quote
    from utils.ai_utils import quotes_prompt

    # Get paper summaries for quote generation
    paper_summaries = [paper.get('content', '') for paper in articles]

    random_quote = quote()
    if random_quote:
        additional_content = f"{random_quote['quote']} --{random_quote['author']}"
    else:
        from utils.models import model_response
        formatted_prompt = quotes_prompt.format(
            paper_summary="\n".join(paper_summaries)
        )
        additional_content = model_response(
            formatted_prompt,
            'claude4',
            max_tokens=1024
        ).strip()

    # Send to Google Chat
    add_log("💬 Sending to Google Chat...")
    thread_key = str(uuid.uuid4())
    start_thread(current_date, additional_content, thread_key)
    time.sleep(0.2)
    send_articles(articles, thread_key)

    # Generate HTML
    add_log("📄 Generating HTML pages...")
    create_subpage(current_date, articles)

    # Update index
    add_log("📑 Updating index page...")
    pages_dir = 'dailies/pages'
    if os.path.exists(pages_dir):
        existing_dates = [f.split('.html')[0] for f in os.listdir(pages_dir) if f.endswith('.html')]
    else:
        existing_dates = []
    if current_date not in existing_dates:
        existing_dates.append(current_date)
    update_index_page(existing_dates)

    # Push to GitHub
    if TEST == 'FALSE':
        add_log("📤 Pushing to GitHub...")
        push_to_github()
        add_log("✅ ALL DONE! Pushed to GitHub")
    else:
        add_log("✅ ALL DONE! (TEST mode - no GitHub push)")

    return get_log_text()


def check_if_ready(daily_total):
    """Check if we have enough papers to show the finish button."""
    return gr.update(visible=len(processed_papers) >= daily_total)


def create_ui():
    """Create the Gradio UI."""

    with gr.Blocks(title="Daily Papers Selector") as ui:
        gr.Markdown("# 📚 Daily Papers - One at a Time")
        gr.Markdown("**Process papers individually and see results in real-time**")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Controls")

                load_btn = gr.Button("🔄 Load Papers", variant="primary", size="lg")

                daily_total = gr.Slider(1, 10, value=3, step=1, label="Daily Total Papers")
                model = gr.Dropdown(["claude4", "claude35"], value="claude4", label="AI Model")

                generate_btn = gr.Button("🚀 Generate This Paper", variant="secondary", size="lg")

                finish_btn = gr.Button(
                    "✅ Finish & Send",
                    variant="primary",
                    size="lg",
                    visible=False
                )

                gr.Markdown("---")
                gr.Markdown("### 📋 Processing Log")
                log_box = gr.Textbox(
                    label="Status",
                    lines=20,
                    interactive=False,
                    value="Click 'Load Papers' to start...",
                    max_lines=20
                )

            with gr.Column(scale=2):
                gr.Markdown("### 📄 Select Paper to Process")
                paper_choice = gr.Radio(
                    choices=[],
                    label="Available Papers (select ONE)",
                    interactive=True
                )

                gr.Markdown("### 📖 Paper Preview")
                paper_preview = gr.Markdown(
                    value="*Select a paper above to see details and arXiv link*"
                )

                gr.Markdown("""
                ---
                **How to use:**
                1. Click **Load Papers** to fetch unseen papers from HuggingFace
                2. Select ONE paper from the list - preview appears with arXiv link
                3. Click **Generate This Paper** and wait for completion
                4. Repeat steps 2-3 until you reach the daily total
                5. Click **Finish & Send** when it appears
                """)

        # Event handlers
        load_btn.click(
            load_papers,
            outputs=[paper_choice, log_box, finish_btn, paper_preview]
        )

        paper_choice.change(
            show_paper_preview,
            inputs=[paper_choice],
            outputs=[paper_preview]
        )

        generate_btn.click(
            process_single_paper,
            inputs=[paper_choice, model],
            outputs=[log_box, finish_btn]
        ).then(
            check_if_ready,
            inputs=[daily_total],
            outputs=[finish_btn]
        )

        finish_btn.click(
            finish_and_send,
            inputs=[daily_total],
            outputs=[log_box]
        )

    return ui


if __name__ == "__main__":
    logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

    ui = create_ui()
    logger.info("Starting UI on http://localhost:7860")

    ui.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True
    )
