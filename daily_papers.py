import os
import re
import json
import uuid
import time
import subprocess
from string import Template 
from tqdm import tqdm
from loguru import logger
from datetime import date
from threading import Thread
from queue import Queue, Empty


from daily_paper_utils import (
    find_not_proposed_papers,
    get_huggingface_papers,
    client_anthropics,
    process_paper,
    send_articles,
    start_thread,
    fetch_data
)

from daily_paper_utils import (
    quotes_prompt,
    provider,
    model
)

# HTML 模板：主页面，使用 $ 作为占位符
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Paper</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            margin: 10px 0;
        }
        a {
            text-decoration: none;
            color: #1a73e8;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Daily Paper</h1>
    <ul>
        $date_links
    </ul>
</body>
</html>
"""


# HTML 模板：子页面，使用 $ 作为占位符
SUBPAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$date Papers</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #333;
        }
        .paper-card {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
            transition: transform 0.2s, box-shadow 0.2s; /* Smooth transition for hover effect */
        }
        .paper-card:hover {
            transform: translateY(-5px); /* Lift effect on hover */
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); /* Shadow on hover */
        }
        .paper-card h2 {
            margin: 0 0 10px;
            font-size: 1.2em;
        }
        .paper-card p {
            margin: 5px 0;
        }
        .paper-card a {
            color: #1a73e8;
            text-decoration: none;
        }
        .paper-card a:hover {
            text-decoration: underline;
        }
        .category-chunk {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            transition: transform 0.2s, box-shadow 0.2s; /* Smooth transition for hover effect */
        }
        .category-chunk:hover {
            transform: translateY(-3px); /* Slightly smaller lift for categories */
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15); /* Slightly smaller shadow for categories */
        }
        .category-chunk:nth-child(1) { /* 1. Topic and Domain */
            background-color: #d3e3fd; /* Blue */
        }
        .category-chunk:nth-child(2) { /* 2. Previous Research and New Ideas */
            background-color: #e6d6fa; /* Purple */
        }
        .category-chunk:nth-child(3) { /* 3. Problem */
            background-color: #d4f8d9; /* Green */
        }
        .category-chunk:nth-child(4) { /* 4. Methods */
            background-color: #ffd7d5; /* Pink */
        }
        .category-chunk:nth-child(5) { /* 5. Results and Evaluation */
            background-color: #d3e3fd; /* Reuse Blue */
        }
    </style>
</head>
<body>
    <h1>$date Papers</h1>
    $paper_content
</body>
</html>
"""

def extract_categories(text):
    """
    Extract the 5 categories and their content from a formatted text string.
    
    Each category is identified by its unique emoji (📘, 💡, ❓, 🛠️, 📊) regardless of the
    exact title text. The function maps these to standardized category names.
    
    Args:
        text (str): The input text containing the 5 categories
        
    Returns:
        dict: A dictionary with standardized category titles as keys and their content as values
    """
    # Define patterns based on emojis only, not the category titles
    patterns = [
        (r'\d+\.\s+\*\*📘.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "📘 Topic and Domain",),
        (r'\d+\.\s+\*\*💡.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "💡 Previous Research and New Ideas"),
        (r'\d+\.\s+\*\*❓.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "❓ Problem"),
        (r'\d+\.\s+\*\*🛠️.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "🛠️ Methods"),
        (r'\d+\.\s+\*\*📊.*?\*\*\s+(.*?)(?=\n\n|\Z)', "📊 Results and Evaluation")
    ]
    
    # Create a dictionary to store results
    results = []
    
    # Apply each pattern and store results with standardized category names
    for pattern, category_name in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            results.append((category_name, match.group(1).strip()))    
    return results

def generate_paper_html(articles):
    """生成子页面的论文内容 HTML，与 Google Chat 推送内容一致"""
    logger.debug(articles)
    paper_html = ""
    for idx, article in enumerate(articles):
        title = article.get('title', 'No Title')
        published_at = article.get('published_at', 'No Date')
        url = article.get('url', '#')
        content = article.get('content', 'No Content')
        categories = extract_categories(content)
        logger.debug(categories)
        # 为每个类别添加 div 和样式
        content_html = ""
        for cat_idx, (cat, cat_content) in enumerate(categories):
            content_html += f"""<div class="category-chunk">{cat_idx+1}.  <strong>{cat}:</strong> {cat_content}</div>"""

        paper_html += f"""
        <div class="paper-card">
            <h2>Paper: {idx+1}</h2>
            <p><strong>{title}</strong></p>
            <p><strong>Published: </strong>{published_at}</p>
            <p><strong>Link: </strong><a href="{url}" target="_blank">{url}</a></p>
            <div>{content_html}</div>
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
            additional_content = client_anthropics.create_message(
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
    push_to_github()
