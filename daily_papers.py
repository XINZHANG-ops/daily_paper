import os
import json
import uuid
import time
import random
import subprocess
from tqdm import tqdm
from loguru import logger
from datetime import date
from threading import Thread
from queue import Queue, Empty
from dotenv import load_dotenv
from inspirational_quotes import quote


from utils import (
    find_not_proposed_papers,
    get_huggingface_papers,
    extract_categories,
    extract_categories_zh,
    generate_daily_tips,
    send_articles,
    start_thread,
    model_response,
    process_paper
)

from utils.file_utils import fetch_data
from utils.ai_utils import quotes_prompt
from utils.template_loader import get_index_template, get_subpage_template


load_dotenv()
TEST = os.getenv("TEST")


def _build_quiz_popup_html(q_idx, q_data, lang):
    """Build quiz popup HTML for a single question in a given language."""
    question = q_data.get('question', 'No Question')
    options = []
    option_keys = sorted(k for k in q_data.keys() if k.startswith('option'))
    for opt_key in option_keys:
        options.append(q_data[opt_key])

    answer_key = q_data.get('answer', '')
    answer_value = ''
    if answer_key.startswith('option'):
        option_index = int(answer_key[6:]) - 1
        if 0 <= option_index < len(options):
            answer_value = options[option_index]

    choices_html = '<div class="quiz-choices">'
    for choice in options:
        choice_class = "quiz-choice long-text" if len(choice) > 100 else "quiz-choice"
        choices_html += f'<div class="{choice_class}" data-value="{choice}">{choice}</div>'
    choices_html += '</div>'

    hide = ' style="display:none"' if lang == 'zh' else ''
    return f'''<div class="quiz-popup" data-answer="{answer_value}" data-lang="{lang}"{hide}>
                        <div class="quiz-question">{q_idx+1}. {question}</div>
                        {choices_html}
                        <div class="quiz-feedback"></div>
                    </div>'''


def generate_paper_html(articles):
    """生成子页面的论文内容 HTML（双语支持）"""
    bg_folder = "bg"
    bg_images = [f for f in os.listdir(bg_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if not bg_images:
        logger.warning("No background images found in the 'bg' folder. Using default background.")

    paper_html = ""
    for idx, article in enumerate(articles):
        title = article.get('title', 'No Title')
        published_at = article.get('published_at', 'No Date')
        url = article.get('url', '#')
        content_en = article.get('content', 'No Content')
        content_zh = article.get('content_zh', '')
        questions_en = article.get('questions', {})
        questions_zh = article.get('questions_zh', {})
        flowchart = article.get('flow_chart', "")

        # EN content
        content_html_en = ""
        for cat_idx, (cat, cat_content) in enumerate(extract_categories(content_en)):
            content_html_en += f'<div class="category-chunk" data-lang="en">{cat_idx+1}.  <strong>{cat}:</strong> {cat_content}</div>'

        # ZH content
        content_html_zh = ""
        if content_zh:
            for cat_idx, (cat, cat_content) in enumerate(extract_categories_zh(content_zh)):
                content_html_zh += f'<div class="category-chunk" data-lang="zh" style="display:none">{cat_idx+1}.  <strong>{cat}:</strong> {cat_content}</div>'

        content_html = content_html_en + content_html_zh

        # Background
        if bg_images:
            selected_bg = random.choice(bg_images)
            bg_style = f"background-image: url('{bg_folder}/{selected_bg}');"
        else:
            bg_style = ""

        # Quiz tabs (bilingual)
        quiz_tabs_html = ""
        if questions_en:
            quiz_tabs_html = '<div class="quiz-tabs">'
            question_items_en = sorted((k, v) for k, v in questions_en.items() if k.startswith('question'))

            for q_idx, (q_key, q_data_en) in enumerate(question_items_en):
                popup_en = _build_quiz_popup_html(q_idx, q_data_en, 'en')
                q_data_zh = questions_zh.get(q_key, {})
                popup_zh = _build_quiz_popup_html(q_idx, q_data_zh, 'zh') if q_data_zh else ''

                quiz_tabs_html += f'''
                <div class="quiz-tab" title="Click To Open Question #{q_idx+1}">Q{q_idx+1}
                    {popup_en}
                    {popup_zh}
                </div>
                '''
            quiz_tabs_html += '</div>'

        # Paper card
        if flowchart:
            paper_html += f"""
            <div class="paper-container">
                <div class="card-deck">
                    <div class="card-counter">1/2</div>
                    <div class="paper-card active" style="{bg_style}">
                        <h2 style="color: #ffffff;">Paper {idx+1}</h2>
                        <p style="color: #badb12;"><strong>{title}</strong></p>
                        <p style="color: #ffffff;"><strong>Published: </strong>{published_at}</p>
                        <p><strong>Link: </strong><a href="{url}" target="_blank">{url}</a></p>
                        <div>{content_html}</div>
                    </div>
                    <div class="paper-card flowchart-card" style="background-color: white;">
                        <h2>{title}</h2>
                        {flowchart}
                    </div>
                </div>
                {quiz_tabs_html}
            </div>
            """
        else:
            paper_html += f"""
            <div class="paper-container">
                <div class="paper-card" style="{bg_style}">
                    <h2 style="color: #ffffff;">Paper {idx+1}</h2>
                    <p style="color: #badb12;"><strong>{title}</strong></p>
                    <p style="color: #ffffff;"><strong>Published: </strong>{published_at}</p>
                    <p><strong>Link: </strong><a href="{url}" target="_blank">{url}</a></p>
                    <div>{content_html}</div>
                </div>
                {quiz_tabs_html}
            </div>
            """
    return paper_html


def generate_tips_html(tips_en, tips_zh):
    """生成每日小贴士 HTML（双语）"""
    return f'''
    <div class="daily-tips-section">
        <h2 class="tips-heading">
            <span data-lang="en">Today's Reading Tips</span>
            <span data-lang="zh" style="display:none">今日阅读推荐</span>
        </h2>
        <div class="tips-content" data-lang="en">{tips_en}</div>
        <div class="tips-content" data-lang="zh" style="display:none">{tips_zh}</div>
    </div>
    '''


def update_index_page(dates):
    """更新主页面，添加日期链接，按年/月/日组织"""
    from collections import defaultdict
    from datetime import datetime

    # 组织日期为 year -> month -> days 结构
    date_structure = defaultdict(lambda: defaultdict(list))

    for date_str in dates:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            year = date_obj.year
            month = date_obj.month
            date_structure[year][month].append(date_str)
        except ValueError:
            logger.warning(f"Invalid date format: {date_str}")
            continue

    # 生成HTML结构
    html_content = ""
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    # 按年份降序排列
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

        # 按月份降序排列
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

            # 按日期降序排列
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

    # 生成统计信息
    total_papers = len(dates)
    total_years = len(date_structure)
    stats = f"Total: {total_papers} papers across {total_years} year{'s' if total_years > 1 else ''}"

    # 使用 Template 进行替换
    template = get_index_template()
    index_html = template.substitute(
        date_structure=html_content,
        stats=stats
    )
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

def create_subpage(date_str, articles, tips=None):
    """创建子页面，展示当天的论文内容"""
    paper_content = generate_paper_html(articles)
    tips_content = ''
    if tips:
        tips_content = generate_tips_html(tips.get('tips_en', ''), tips.get('tips_zh', ''))

    template = get_subpage_template()
    subpage_html = template.substitute(
        date=date_str,
        paper_content=paper_content,
        tips_content=tips_content
    )

    os.makedirs('dailies/pages', exist_ok=True)
    with open(f'dailies/pages/{date_str}.html', 'w', encoding='utf-8') as f:
        f.write(subpage_html)

# 主流程
if __name__ == "__main__":
    subprocess.run(["git", "switch", "main"])
    subprocess.run(["git", "pull"])

    max_paper_length = 24000
    rank_method = 'hot'
    paper_counts = 3
    grab_number = 100
    
    summaries = []
    with open('summaries.jsonl', 'r') as file:
        for line in file:
            summaries.append(json.loads(line.strip()))

    current_paper_list = []
    for p in summaries:
        current_paper_list.append(p['title'])
    
    current_date = date.today().strftime("%Y-%m-%d")
    grab_papers = get_huggingface_papers(sort_method=rank_method, limit=grab_number)
    new_papers, _ = find_not_proposed_papers(
        grab_papers=grab_papers,
        current_paper_list=current_paper_list
    )
    
    if len(new_papers) > 0:
        processed = 0
        paper_summaries = []
        THREAD_KEY_VALUE = str(uuid.uuid4())
        articles = []

        for paper in tqdm(new_papers):
            queue = Queue()
            start_time = time.time()
            
            thread = Thread(target=process_paper, args=(paper, queue, max_paper_length))
            thread.daemon = True
            thread.start()
            
            thread.join(timeout=150)
            
            elapsed_time = time.time() - start_time
            
            if thread.is_alive():
                print(f"Processing took over 30 seconds ({elapsed_time:.2f}s), skipping paper.")
                continue
            
            try:
                result = queue.get_nowait()
            except Empty:
                print("No result returned from processing, skipping paper.")
                continue
            
            if result is None:
                continue
            elif isinstance(result, str):
                print(f"Error processing paper: {result}")
                continue
            
            paper_info, summary = result
            logger.debug(summary)
            paper_summaries.append(summary)
            
            if TEST == 'FALSE':
                with open('summaries.jsonl', 'a') as f:
                    paper_info['date'] = current_date
                    f.write(json.dumps(paper_info) + '\n')
            
            articles.append(paper_info)
            
            processed += 1
            
            if processed >= paper_counts:
                break

        quotes_prompt = quotes_prompt.format(
            paper_summary="\n".join(paper_summaries)
        )

        # random_quote = fetch_data("/quotes/random")
        random_quote = quote()
        if random_quote:
            additional_content = f"{random_quote['quote']} --{random_quote['author']}"
        else:
            additional_content = model_response(
                quotes_prompt,
                max_tokens=1024
            ).strip()
        additional_content = f"{additional_content}"
        link = f"https://xinzhang-ops.github.io/daily_paper/dailies/{current_date}.html"
    
        start_thread(current_date, additional_content, THREAD_KEY_VALUE)
        time.sleep(0.2)
        send_articles(articles, THREAD_KEY_VALUE)

        # 生成每日小贴士
        tips = None
        if paper_summaries:
            try:
                tips = generate_daily_tips(paper_summaries)
                tips_dir = 'dailies/tips'
                os.makedirs(tips_dir, exist_ok=True)
                with open(f'{tips_dir}/{current_date}.json', 'w', encoding='utf-8') as f:
                    json.dump(tips, f, ensure_ascii=False)
            except Exception as e:
                logger.error(f"Failed to generate tips: {e}")

        # 生成 GitHub Pages 文件
        # 1. 创建子页面
        create_subpage(current_date, articles, tips=tips)

        # 2. 更新主页面
        pages_dir = 'dailies/pages'
        if os.path.exists(pages_dir):
            existing_dates = [f.split('.html')[0] for f in os.listdir(pages_dir) if f.endswith('.html')]
        else:
            existing_dates = []
        if current_date not in existing_dates:
            existing_dates.append(current_date)
        update_index_page(existing_dates)

    def push_to_github():
        subprocess.run(["git", "add", "index.html", "dailies/pages/", "dailies/notes/", "dailies/images/", "dailies/tips/"])
        subprocess.run(["git", "add", "summaries.jsonl"])
        subprocess.run(["git", "commit", "-m", "Daily Paper Push"])
        subprocess.run(["git", "push", "origin", "main"])
    
    if TEST == "FALSE":
        push_to_github()
