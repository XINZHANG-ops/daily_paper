#!/usr/bin/env python3
"""
Gradio UI for editing daily paper notes with live markdown preview and image support
"""

import gradio as gr
import os
import subprocess
from pathlib import Path
import shutil
from datetime import datetime
import json


def get_image_tag(filename):
    """Generate markdown image tag"""
    return f"\n![My diagram notes]({filename})"


def render_markdown_preview(md_text, date=None, uploaded_images=None):  # pylint: disable=unused-argument
    """Process markdown to fix image paths for preview"""
    if not md_text:
        return ""

    # Fix image paths if date is provided
    if date:
        import re
        # Replace image references to point to the correct location
        # Convert ![alt](filename.png) to ![alt](dailies/images/{date}/filename.png)
        md_text = re.sub(
            r'!\[([^\]]*)\]\((?!http://|https://|/)([^)]+)\)',
            f'![\\1](dailies/images/{date}/\\2)',
            md_text
        )

    # Return the processed markdown - Gradio will handle LaTeX rendering
    return md_text


def add_image_to_notes(md_text, image_files):
    """Add image markdown tags to the end of notes with numbered names"""
    if not image_files:
        return md_text

    # Count existing image references to continue numbering
    import re
    existing_images = re.findall(r'!\[.*?\]\(image_(\d+)\.png\)', md_text)
    if existing_images:
        start_index = max(int(num) for num in existing_images) + 1
    else:
        start_index = 1

    # Add new images with numbered names
    for i, img in enumerate(image_files, start=start_index):
        if img is not None:
            # Get file extension
            ext = os.path.splitext(img.name)[1] or '.png'
            numbered_filename = f"image_{i}{ext}"
            tag = get_image_tag(numbered_filename)
            if tag not in md_text:
                md_text += tag

    return md_text


def save_notes(date, md_text, image_files):
    """Save markdown notes and images to the dailies folder"""
    if not date:
        return "❌ Error: Please enter a date (e.g., 2026-01-10)"

    if not md_text:
        return "❌ Error: Notes cannot be empty"

    # Validate date format
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return f"❌ Error: Invalid date format. Use YYYY-MM-DD (e.g., 2026-01-10)"

    # Create directories
    notes_dir = Path('dailies/notes')
    images_dir = Path(f'dailies/images/{date}')

    notes_dir.mkdir(parents=True, exist_ok=True)

    # Save markdown file
    md_file = notes_dir / f'{date}.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_text)

    # Save images if any with numbered names
    saved_images = []
    if image_files:
        images_dir.mkdir(parents=True, exist_ok=True)

        # Extract image numbers from markdown to match filenames
        import re
        image_refs = re.findall(r'!\[.*?\]\((image_\d+\.[^)]+)\)', md_text)

        for i, img in enumerate(image_files):
            if img is not None:
                # Get the corresponding numbered filename from markdown
                if i < len(image_refs):
                    numbered_filename = image_refs[i]
                else:
                    # Fallback if not found in markdown
                    ext = os.path.splitext(img.name)[1] or '.png'
                    numbered_filename = f"image_{i+1}{ext}"

                dest_path = images_dir / numbered_filename
                shutil.copy2(img.name, dest_path)
                saved_images.append(numbered_filename)

    result = f"✅ Saved successfully!\n\n"
    result += f"📝 Markdown: {md_file}\n"
    if saved_images:
        result += f"🖼️ Images ({len(saved_images)}): {', '.join(saved_images)}\n"
        result += f"📁 Image folder: {images_dir}"

    return result


def update_index_html():
    """Update index.html with note indicators"""
    try:
        from collections import defaultdict
        from string import Template
        import sys
        sys.path.insert(0, str(Path(__file__).parent))

        # Import template loader directly to avoid loading utils package
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "template_loader",
            Path(__file__).parent / "utils" / "template_loader.py"
        )
        template_loader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(template_loader)
        get_index_template = template_loader.get_index_template

        # Get all existing dates from dailies/pages/ directory
        # This is more reliable than reading from summaries.jsonl
        dates = set()
        pages_dir = Path('dailies/pages')

        if pages_dir.exists():
            for page_file in pages_dir.glob('*.html'):
                date_str = page_file.stem  # filename without extension
                dates.add(date_str)

        # Organize dates by year -> month -> days
        date_structure = defaultdict(lambda: defaultdict(list))

        for date_str in dates:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                year = date_obj.year
                month = date_obj.month
                date_structure[year][month].append(date_str)
            except ValueError:
                continue

        # Generate HTML structure
        html_content = ""
        month_names = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }

        # Sort by year descending
        for year in sorted(date_structure.keys(), reverse=True):
            year_papers = sum(len(days) for days in date_structure[year].values())
            html_content += f'''
        <div class="year-container">
            <div class="year-header">
                <span>{year} ({year_papers} papers)</span>
                <span class="arrow">▼</span>
            </div>
            <div class="content">
        '''

            # Sort by month descending
            for month in sorted(date_structure[year].keys(), reverse=True):
                days = date_structure[year][month]
                month_name = month_names[month]
                html_content += f'''
                <div class="month-container">
                    <div class="month-header">
                        <span>{month_name} {year} ({len(days)} papers)</span>
                        <span class="arrow">▼</span>
                    </div>
                    <div class="content">
                        <ul class="day-list">
            '''

                # Sort by date descending
                for date_str in sorted(days, reverse=True):
                    # Check if this date has notes
                    has_notes = os.path.exists(f'dailies/notes/{date_str}.md')
                    note_indicator = ' <span class="note-badge">📝</span>' if has_notes else ''
                    html_content += f'                        <li><a href="dailies/pages/{date_str}.html">{date_str}{note_indicator}</a></li>\n'

                html_content += '''                        </ul>
                    </div>
                </div>
            '''

            html_content += '''            </div>
        </div>
        '''

        # Generate stats
        total_papers = len(dates)
        total_years = len(date_structure)
        stats = f"Total: {total_papers} papers across {total_years} year{'s' if total_years > 1 else ''}"

        # Use template to generate index
        template = get_index_template()
        index_html = template.substitute(
            date_structure=html_content,
            stats=stats
        )

        # Write to index.html
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(index_html)

        return True
    except Exception as e:
        print(f"Error updating index: {e}")
        import traceback
        traceback.print_exc()
        return False


def upload_to_git(date):
    """Git add, commit, and push - also updates index.html"""
    if not date:
        return "❌ Error: Please enter a date for commit message"

    try:
        # First, update index.html to include note indicators
        result_msg = "📋 Updating index.html...\n"
        if update_index_html():
            result_msg += "✅ Index updated with note indicators\n\n"
        else:
            result_msg += "⚠️ Could not update index (will continue with git)\n\n"

        # Check if there are changes
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            check=True
        )

        if not status_result.stdout.strip():
            return result_msg + "ℹ️ No changes to commit"

        # Git add all
        subprocess.run(['git', 'add', '-A'], check=True)

        # Git commit
        commit_result = subprocess.run(
            ['git', 'commit', '-m', date],
            capture_output=True,
            text=True,
            check=True
        )

        # Git push
        push_result = subprocess.run(
            ['git', 'push'],
            capture_output=True,
            text=True,
            check=True
        )

        result_msg += "✅ Successfully uploaded to Git!\n\n"
        result_msg += f"📤 Commit: {date}\n"
        result_msg += f"🔄 Pushed to remote"

        return result_msg

    except subprocess.CalledProcessError as e:
        return f"❌ Git error: {e.stderr if e.stderr else str(e)}"


def get_default_date():
    """Get the most recent date without notes from dailies/pages/"""
    pages_dir = Path('dailies/pages')
    notes_dir = Path('dailies/notes')

    if not pages_dir.exists():
        return datetime.now().strftime('%Y-%m-%d')

    # Get all page dates (without .html extension)
    page_files = sorted(pages_dir.glob('*.html'), reverse=True)

    for page_file in page_files:
        date_str = page_file.stem  # filename without extension
        # Check if this date has notes
        notes_file = notes_dir / f'{date_str}.md'
        if not notes_file.exists():
            return date_str

    # If all pages have notes, return today's date
    return datetime.now().strftime('%Y-%m-%d')


def load_existing_notes(date):
    """Load existing notes for a date if they exist"""
    if not date:
        return "", []

    notes_file = Path(f'dailies/notes/{date}.md')
    if notes_file.exists():
        with open(notes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, f"📂 Loaded existing notes for {date}"

    return "", f"📝 New notes for {date}"


# Create Gradio interface
with gr.Blocks(title="Daily Paper Notes Editor", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 📝 Daily Paper Notes Editor")
    gr.Markdown("Write your daily paper notes with live preview, image support, and Git integration")

    with gr.Row():
        with gr.Column(scale=1):
            date_input = gr.Textbox(
                label="📅 Date",
                placeholder="2026-01-10",
                value=get_default_date(),
                info="Format: YYYY-MM-DD (Default: latest date without notes)"
            )

            load_btn = gr.Button("📂 Load Existing Notes", variant="secondary")
            load_status = gr.Textbox(label="Status", interactive=False, show_label=False)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ✍️ Write Notes")

            notes_input = gr.Textbox(
                label="Markdown Notes",
                placeholder="# For paper **Title**\n\nYour notes here...\n\nUse $...$ for inline math and $$...$$ for display math",
                lines=20,
                max_lines=30,
                show_label=False
            )

            gr.Markdown("### 🖼️ Images (Drag & Drop)")
            image_gallery = gr.File(
                label="Drop images here",
                file_count="multiple",
                file_types=["image"],
                type="filepath"
            )

            with gr.Row():
                save_btn = gr.Button("💾 Save", variant="primary", scale=2)
                upload_btn = gr.Button("📤 Git Upload", variant="stop", scale=1)

            save_status = gr.Textbox(label="Save Status", interactive=False, lines=5)

        with gr.Column(scale=1):
            gr.Markdown("### 👁️ Live Preview")
            preview_output = gr.Markdown(
                value="Start typing to see preview...",
                latex_delimiters=[
                    {"left": "$$", "right": "$$", "display": True},
                    {"left": "$", "right": "$", "display": False}
                ]
            )

    # Event handlers
    def update_preview(md_text, date, images):
        return render_markdown_preview(md_text, date, images)

    def handle_image_upload(md_text, images):
        return add_image_to_notes(md_text, images)

    # Load existing notes
    load_btn.click(
        fn=load_existing_notes,
        inputs=[date_input],
        outputs=[notes_input, load_status]
    )

    # Update preview on text change
    notes_input.change(
        fn=update_preview,
        inputs=[notes_input, date_input, image_gallery],
        outputs=[preview_output]
    )

    # Update preview on date change
    date_input.change(
        fn=update_preview,
        inputs=[notes_input, date_input, image_gallery],
        outputs=[preview_output]
    )

    # Handle image upload - add tags and update preview
    image_gallery.change(
        fn=handle_image_upload,
        inputs=[notes_input, image_gallery],
        outputs=[notes_input]
    ).then(
        fn=update_preview,
        inputs=[notes_input, date_input, image_gallery],
        outputs=[preview_output]
    )

    # Save button
    save_btn.click(
        fn=save_notes,
        inputs=[date_input, notes_input, image_gallery],
        outputs=[save_status]
    )

    # Upload button
    upload_btn.click(
        fn=upload_to_git,
        inputs=[date_input],
        outputs=[save_status]
    )

    # Initial preview
    app.load(
        fn=update_preview,
        inputs=[notes_input, date_input, image_gallery],
        outputs=[preview_output]
    )

if __name__ == "__main__":
    app.launch(
        server_name="127.0.0.1",
        server_port=7861,
        share=False
    )