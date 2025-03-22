import os
import json
import uuid
import time
import random
import subprocess
from tqdm import tqdm
from loguru import logger
from datetime import date
from string import Template 
from threading import Thread
from queue import Queue, Empty
from dotenv import load_dotenv


from daily_paper_utils import (
    find_not_proposed_papers,
    get_huggingface_papers,
    extract_categories,
    process_paper,
    send_articles,
    start_thread,
    client_llm,
    fetch_data
)

from daily_paper_utils import (
    quotes_prompt,
    provider,
    model
)

from html_temps import (
    INDEX_TEMPLATE,
    SUBPAGE_TEMPLATE
)


load_dotenv()
TEST = os.getenv("TEST")


def generate_paper_html(articles):
    """生成子页面的论文内容 HTML，与 Google Chat 推送内容一致"""
    # 获取 bg 文件夹中的所有图片文件
    bg_folder = "bg"
    bg_images = [f for f in os.listdir(bg_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if not bg_images:
        logger.warning("No background images found in the 'bg' folder. Using default background.")
    
    logger.debug(articles)
    paper_html = ""
    for idx, article in enumerate(articles):
        title = article.get('title', 'No Title')
        published_at = article.get('published_at', 'No Date')
        url = article.get('url', '#')
        content = article.get('content', 'No Content')
        questions_dict = article.get('questions', {})  # 获取问题字典
        categories = extract_categories(content)
        logger.debug(categories)
        
        # 为每个类别添加 div 和样式
        content_html = ""
        for cat_idx, (cat, cat_content) in enumerate(categories):
            content_html += f"""<div class="category-chunk">{cat_idx+1}.  <strong>{cat}:</strong> {cat_content}</div>"""

        # 随机选择一个背景图片
        if bg_images:
            selected_bg = random.choice(bg_images)
            bg_style = f"background-image: url('{bg_folder}/{selected_bg}');"
        else:
            bg_style = ""  # Fallback to default background if no images are found
        
        # 生成问题标签HTML
        quiz_tabs_html = ""
        if questions_dict:
            quiz_tabs_html = '<div class="quiz-tabs">'
            
            # 处理新的问题格式
            question_items = [(k, v) for k, v in questions_dict.items() if k.startswith('question')]
            question_items.sort()  # 确保问题按顺序排列
            
            for q_idx, (q_key, q_data) in enumerate(question_items):
                question = q_data.get('question', 'No Question')
                
                # 获取选项
                options = []
                option_keys = [k for k in q_data.keys() if k.startswith('option')]
                option_keys.sort()  # 确保选项按顺序排列
                
                for opt_key in option_keys:
                    options.append(q_data[opt_key])
                
                answer_key = q_data.get('answer', '')  # 例如 'option2'
                answer_value = ''
                
                # 获取正确答案的值
                if answer_key.startswith('option'):
                    option_index = int(answer_key[6:]) - 1  # 从'option2'获取索引1
                    if 0 <= option_index < len(options):
                        answer_value = options[option_index]
                
                # 生成选项HTML
                choices_html = '<div class="quiz-choices">'
                for choice_idx, choice in enumerate(options):
                    choice_class = "quiz-choice"
                    if len(choice) > 100:  # 如果选项文本非常长
                        choice_class += " long-text"
                    
                    choices_html += f'<div class="{choice_class}" data-value="{choice}">{choice}</div>'
                choices_html += '</div>'
                
                # 生成完整的问题标签
                quiz_tabs_html += f'''
                <div class="quiz-tab" title="点击查看问题 #{q_idx+1}">Q{q_idx+1}
                    <div class="quiz-popup" data-answer="{answer_value}">
                        <div class="quiz-question">{q_idx+1}. {question}</div>
                        {choices_html}
                        <div class="quiz-feedback"></div>
                    </div>
                </div>
                '''
            quiz_tabs_html += '</div>'

        paper_html += f"""
        <div class="paper-container">
            <div class="paper-card" style="{bg_style}">
                <h2>Paper {idx+1}</h2>
                <p><strong>{title}</strong></p>
                <p><strong>Published: </strong>{published_at}</p>
                <p><strong>Link: </strong><a href="{url}" target="_blank">{url}</a></p>
                <div>{content_html}</div>
            </div>
            {quiz_tabs_html}
        </div>
        """
    return paper_html

def update_index_page(dates):
    """更新主页面，添加日期链接"""
    date_links = ""
    for d in sorted(dates, reverse=True):  # 按日期降序排列
        date_links += f'<li><a href="{d}.html">{d}</a></li>\n'
    
    # 使用 Template 进行替换
    template = Template(INDEX_TEMPLATE)
    index_html = template.substitute(date_links=date_links)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

def create_subpage(date_str, articles):
    """创建子页面，展示当天的论文内容"""
    paper_content = generate_paper_html(articles)
    
    # 使用 Template 进行替换
    template = Template(SUBPAGE_TEMPLATE)
    subpage_html = template.substitute(date=date_str, paper_content=paper_content)
    with open(f'{date_str}.html', 'w', encoding='utf-8') as f:
        f.write(subpage_html)

# 主流程
if __name__ == "__main__":
    max_paper_length = 12000
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
            
            thread.join(timeout=30)
            
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
                    f.write(json.dumps(paper_info) + '\n')
            
            articles.append(paper_info)
            
            processed += 1
            
            if processed >= paper_counts:
                break

        quotes_prompt = quotes_prompt.format(
            paper_summary="\n".join(paper_summaries)
        )

        random_quote = fetch_data("/quotes/random")
        if random_quote:
            additional_content = f"{random_quote[0]['content']} --{random_quote[0]['author']}"
        else:
            additional_content = client_llm.create_message(
                messages=[{
                    "role": "user",
                    "content": quotes_prompt
                }],
                max_tokens=1024,
                provider=provider,
                model=model,
                version=None
            )['message']['content'].strip()

        additional_content = f"{additional_content}"
        link = f"https://xinzhang-ops.github.io/daily_paper/{current_date}.html"
    
        start_thread(current_date, additional_content, THREAD_KEY_VALUE)
        time.sleep(0.2)
        send_articles(articles, THREAD_KEY_VALUE)

        # 生成 GitHub Pages 文件
        # 1. 创建子页面
        create_subpage(current_date, articles)

        # 2. 更新主页面
        existing_dates = [f.split('.html')[0] for f in os.listdir() if f.endswith('.html') and f != 'index.html']
        if current_date not in existing_dates:
            existing_dates.append(current_date)
        update_index_page(existing_dates)

    def push_to_github():
        subprocess.run(["git", "add", "index.html", "*.html"])
        subprocess.run(["git", "commit", "-m", "Daily Paper Push"])
        subprocess.run(["git", "push", "origin", "main"])
    
    if TEST == "FALSE":
        push_to_github()
