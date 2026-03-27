"""
AI Generation Utilities

This module provides functions for AI-powered content generation including paper summaries,
question creation, flowchart generation, and text parsing. It uses various AI models to
analyze academic papers and create structured outputs.
"""

import re
import json
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
from .models import model_response


# Prompts for AI generation
PROMPT = """
You are a research expert skilled at reading academic papers.
Provide an analysis of this paper by answering only the following questions, and answer each question in one concise sentence:
1. What is the topic and domain of the paper?
2. What previous research is the paper based on, and what new ideas does it propose?
3. What problem does the paper aim to solve?
4. What method(s) did the authors use?
5. What were the results, and how were they evaluated?

Here is the paper:
Title: {title}

Content:
{content}

Follow this format of your output(reply with these 5 topics concisely and nothing else):
1.  **📘 Topic and Domain:** The paper's topic and domain.

2.  **💡 Previous Research and New Ideas:** The paper based on and new idea.

3.  **❓ Problem:** The problem the paper solves.

4.  **🛠️ Methods:** The method the paper uses.

5.  **📊 Results and Evaluation:** The results.
"""


QUESTION_PROMPT = """
You are a research expert skilled at reading academic papers.
Here is the paper:
Title: {title}

Content:
{content}

And here is a summary of the paper:
{summary}

--------------
Your job is to create 3 multiple choices questions about the paper like a short quiz.
It can about the problem solved of the paper, the method of the paper or impact of the paper or literally anything about the paper.
Each question should has only 3 options, for each question you should generate the question, options and the correct answer.
Try to be creative on your question and options.

Follow exactly the format below for your outputs:

"""


QUESTION_FORMAT = """
{
  "question1": {
    "question": "question statemant",
    "option1": "option1 statement",
    "option2": "option2 statement",
    "option3": "option3 statement",
    "answer": "option1 or option2 or option3"
  },
  "question2": {
    "question": "question statemant",
    "option1": "option1 statement",
    "option2": "option2 statement",
    "option3": "option3 statement",
    "answer": "option1 or option2 or option3"
  },
  "question3": {
    "question": "question statemant",
    "option1": "option1 statement",
    "option2": "option2 statement",
    "option3": "option3 statement",
    "answer": "option1 or option2 or option3"
  }
}
Notice you need to generate 3 questions as shown above, you must follow the exact format, for each question the keys include the question text, 3 options, and the answer, do not miss any "delimiter".
Now output your the questions and nothing else:
"""


FLOW_CHART_PROMPT = """
You are a research assistant. You job is to help me to create a flow chart of the paper content.
Since it is about the workflow of the paper, your focus is the method applied in the paper.

Your should contain your answer in a SVG format as following format:
<format>
you should have your output with this specific <svg> tag.

<svg width="100%" viewBox="0 0 1000 800">
Here are the content you can create freely, use all shapes, text format or styles as you like.
Try to be creative, and make it look good and colorful.
Try use less arrows, since the arrow you give tends to be messy.
</svg>

</format>

Here is the content of the paper "{title}":
<content>
{article_content}
</content>

Now please give me the SVG format of the flow chart, you should only give me the SVG format directly, do not output backticks for formatting, no other text.
"""


PROMPT_BILINGUAL = """
You are a research expert skilled at reading academic papers.
Provide an analysis of this paper by answering only the following questions, and answer each question in one concise sentence.
You must provide the analysis in BOTH English and Chinese.

Here is the paper:
Title: {title}

Content:
{content}

Output format (output BOTH sections, nothing else):

===EN===
1.  **📘 Topic and Domain:** The paper's topic and domain.

2.  **💡 Previous Research and New Ideas:** The paper based on and new idea.

3.  **❓ Problem:** The problem the paper solves.

4.  **🛠️ Methods:** The method the paper uses.

5.  **📊 Results and Evaluation:** The results.

===ZH===
1.  **📘 主题与领域：** 论文的主题和领域。

2.  **💡 先前研究与新思路：** 基于的研究和新想法。

3.  **❓ 问题：** 论文解决的问题。

4.  **🛠️ 方法：** 论文使用的方法。

5.  **📊 结果与评估：** 结果。
"""


QUESTION_PROMPT_BILINGUAL = """
You are a research expert skilled at reading academic papers.
Here is the paper:
Title: {title}

Content:
{content}

And here is a summary of the paper:
{summary}

--------------
Create 3 multiple choice questions about the paper in BOTH English and Chinese.
Each question has only 3 options. Be creative.

Output valid JSON only (no other text, no markdown backticks):
{{
  "en": {{
    "question1": {{"question": "English question", "option1": "opt1", "option2": "opt2", "option3": "opt3", "answer": "option1 or option2 or option3"}},
    "question2": {{"question": "English question", "option1": "opt1", "option2": "opt2", "option3": "opt3", "answer": "option1 or option2 or option3"}},
    "question3": {{"question": "English question", "option1": "opt1", "option2": "opt2", "option3": "opt3", "answer": "option1 or option2 or option3"}}
  }},
  "zh": {{
    "question1": {{"question": "中文题目", "option1": "选项1", "option2": "选项2", "option3": "选项3", "answer": "option1 or option2 or option3"}},
    "question2": {{"question": "中文题目", "option1": "选项1", "option2": "选项2", "option3": "选项3", "answer": "option1 or option2 or option3"}},
    "question3": {{"question": "中文题目", "option1": "选项1", "option2": "选项2", "option3": "选项3", "answer": "option1 or option2 or option3"}}
  }}
}}
"""


TIPS_PROMPT = """
You are a research advisor. Based on the summaries of today's papers below, write a brief reading recommendation (2-3 sentences max).
Suggest which paper to read first and why, and note any connections between the papers.

Papers:
{summaries}

Output valid JSON only, no other text, no markdown backticks:
{{"tips_en": "Your English recommendation here.", "tips_zh": "你的中文推荐内容。"}}
"""


quotes_prompt = """
You are a knowledgeable quote expert.
Based on the context below, you give me a famous quote of my day.

<Context>
{paper_summary}
</Context>

The Quote should be the format of:
"the quote --person name"

Now Output Your Quote(do not output anything else exception for the Quote):
""".strip()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def summary_paper(paper_title, paper_content, model_name=None):
    """
    Generate a structured summary of an academic paper.

    This function uses an AI model to analyze a paper and provide a concise summary
    covering five key aspects: topic, previous research, problem, methods, and results.

    Args:
        paper_title (str): The title of the paper
        paper_content (str): The full text content of the paper
        model_name (str): The model to use ('claude4' or 'claude35')

    Returns:
        str: A formatted summary with five categorized sections
    """
    logger.debug(f'Creating summary for "{paper_title}" using {model_name}')
    prompt = PROMPT.format(
        title=paper_title,
        content=paper_content
    )
    logger.debug(f"Prompt length: {len(prompt.split(' '))}")

    summary = model_response(
        prompt,
        model_name,
        max_tokens=8000

    )
    return summary


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def create_question(paper_title, paper_content, summary, model_name=None):
    """
    Generate quiz questions about an academic paper.

    Creates three multiple-choice questions based on the paper content and summary,
    testing understanding of key concepts, methods, or findings.

    Args:
        paper_title (str): The title of the paper
        paper_content (str): The full text content of the paper
        summary (str): A summary of the paper
        model_name (str): The model to use ('claude4' or 'claude35')

    Returns:
        dict: A dictionary containing three questions with options and answers
    """
    logger.debug(f'Creating question for "{paper_title}" using {model_name}')
    prompt = QUESTION_PROMPT.format(
        title = paper_title,
        content = paper_content,
        summary = summary,
    ) + QUESTION_FORMAT

    questions_content = model_response(
        prompt,
        model_name,
        max_tokens=8000

    )
    logger.debug(questions_content)
    questions = parse_output(questions_content)
    return questions


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def create_flow_chart(paper_title, paper_content, model_name=None):
    """
    Generate an SVG flowchart visualizing the paper's methodology.

    Creates a visual flowchart representation of the paper's workflow and methods
    in SVG format.

    Args:
        paper_title (str): The title of the paper
        paper_content (str): The full text content of the paper
        model_name (str): The model to use ('claude4' or 'claude35')

    Returns:
        str: SVG markup representing the flowchart
    """
    logger.debug(f'Creating flow chart for "{paper_title}" using {model_name}')
    prompt = FLOW_CHART_PROMPT.format(
        title=paper_title,
        article_content=paper_content
    )
    flow_chart = model_response(
        prompt,
        model_name,
        max_tokens=8192

    )
    return parse_flowchart(flow_chart)


def extract_categories(text):
    """
    Extract the 5 categories and their content from a formatted text string.

    Each category is identified by its unique emoji (📘, 💡, ❓, 🛠️, 📊) regardless of the
    exact title text. The function maps these to standardized category names.

    Args:
        text (str): The input text containing the 5 categories

    Returns:
        list: A list of tuples with (category_name, content) pairs
    """
    # Define patterns based on emojis only, not the category titles
    patterns = [
        (r'\d+\.\s+\*\*📘.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "📘 Topic and Domain",),
        (r'\d+\.\s+\*\*💡.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "💡 Previous Research and New Ideas"),
        (r'\d+\.\s+\*\*❓.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "❓ Problem"),
        (r'\d+\.\s+\*\*🛠️.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "🛠️ Methods"),
        (r'\d+\.\s+\*\*📊.*?\*\*\s+(.*?)(?=\n\n|\Z)', "📊 Results and Evaluation")
    ]

    # Create a list to store results
    results = []

    # Apply each pattern and store results with standardized category names
    for pattern, category_name in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            results.append((category_name, match.group(1).strip()))
    return results


def extract_categories_zh(text):
    """Extract 5 categories from Chinese formatted summary text."""
    patterns = [
        (r'\d+\.\s+\*\*📘.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "📘 主题与领域"),
        (r'\d+\.\s+\*\*💡.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "💡 先前研究与新思路"),
        (r'\d+\.\s+\*\*❓.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "❓ 问题"),
        (r'\d+\.\s+\*\*🛠️.*?\*\*\s+(.*?)(?=\n\n\d+\.|\Z)', "🛠️ 方法"),
        (r'\d+\.\s+\*\*📊.*?\*\*\s+(.*?)(?=\n\n|\Z)', "📊 结果与评估")
    ]
    results = []
    for pattern, category_name in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            results.append((category_name, match.group(1).strip()))
    return results


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def summary_paper_bilingual(paper_title, paper_content, model_name=None):
    """Generate bilingual (EN+ZH) summary in a single model call."""
    logger.debug(f'Creating bilingual summary for "{paper_title}"')
    prompt = PROMPT_BILINGUAL.format(title=paper_title, content=paper_content)
    response = model_response(prompt, model_name, max_tokens=8000)

    summary_en, summary_zh = response, ''
    if '===ZH===' in response:
        parts = response.split('===ZH===')
        summary_en = parts[0].replace('===EN===', '').strip()
        summary_zh = parts[1].strip()
    elif '===EN===' in response:
        summary_en = response.split('===EN===')[-1].strip()

    return summary_en, summary_zh


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def create_question_bilingual(paper_title, paper_content, summary, model_name=None):
    """Generate bilingual (EN+ZH) quiz questions in a single model call."""
    logger.debug(f'Creating bilingual questions for "{paper_title}"')
    prompt = QUESTION_PROMPT_BILINGUAL.format(
        title=paper_title,
        content=paper_content,
        summary=summary,
    )
    response = model_response(prompt, model_name, max_tokens=8000)
    parsed = parse_output(response)
    questions_en = parsed.get('en', parsed)
    questions_zh = parsed.get('zh', {})
    return questions_en, questions_zh


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generate_daily_tips(summaries_list, model_name=None):
    """Generate bilingual daily reading tips from paper summaries."""
    logger.debug('Generating daily tips')
    combined = "\n\n---\n\n".join(summaries_list)
    prompt = TIPS_PROMPT.format(summaries=combined)
    response = model_response(prompt, model_name, max_tokens=2000)
    return parse_output(response)


def find_json_content(text):
    """
    Extract JSON content from markdown code blocks.

    Args:
        text (str): Text containing ```json code blocks

    Returns:
        str: The JSON content without markdown formatting
    """
    pattern = r'```json\s*([\s\S]*?)\s*```'
    matches = re.findall(pattern, text)
    return matches[0]


def find_svg_content(text):
    """
    Extract SVG content from markdown code blocks.

    Args:
        text (str): Text containing ```svg code blocks

    Returns:
        str: The SVG content without markdown formatting
    """
    pattern = r'```svg\s*([\s\S]*?)\s*```'
    matches = re.findall(pattern, text)
    return matches[0]


def find_xml_content(text):
    """
    Extract XML content from markdown code blocks.

    Args:
        text (str): Text containing ```xml code blocks

    Returns:
        str: The XML content without markdown formatting
    """
    pattern = r'```xml\s*([\s\S]*?)\s*```'
    matches = re.findall(pattern, text)
    return matches[0]


def parse_output(output: str) -> dict:
    """
    Parse JSON output from AI responses, handling markdown code blocks.

    Args:
        output (str): AI response that may contain JSON in code blocks

    Returns:
        dict: Parsed JSON as a Python dictionary
    """
    if '```json' in output:
        output = find_json_content(output)
    return json.loads(output)


def parse_flowchart(output: str) -> str:
    """
    Parse SVG/XML flowchart output from AI responses.

    Args:
        output (str): AI response that may contain SVG/XML in code blocks

    Returns:
        str: SVG/XML content without markdown formatting
    """
    if '```svg' in output:
        output = find_svg_content(output)

    if '```xml' in output:
        output = find_xml_content(output)
    return output


def process_paper(paper, queue, max_paper_length, model_name=None):
    """
    Process a single paper: download, summarize, create quiz, generate flowchart.

    This function runs in a thread and puts the result in a queue.

    Args:
        paper (dict): Paper information from HuggingFace
        queue (Queue): Thread-safe queue to store results
        max_paper_length (int): Maximum word count for papers
        model_name (str): The model to use ('claude4' or 'claude35')
    """
    from .arxiv_utils import download_paper_text

    try:
        paper_data = download_paper_text(paper)
        published_at = paper['published_at'][:10]
        title = paper['title']
        paper_url = paper_data['pdf_url']
        content = paper_data['text']

        if len(content.split(' ')) > max_paper_length:
            queue.put(None)  # Signal to skip this paper
            return

        summary_en, summary_zh = summary_paper_bilingual(title, content, model_name)
        questions_en, questions_zh = create_question_bilingual(
            paper_title=title,
            paper_content=content,
            summary=summary_en,
            model_name=model_name
        )
        flow_chart = create_flow_chart(
            paper_title=title,
            paper_content=content,
            model_name=model_name
        )

        paper_info = {
            'title': title,
            'published_at': published_at,
            'url': paper_url,
            'content': summary_en,
            'content_zh': summary_zh,
            'questions': questions_en,
            'questions_zh': questions_zh,
            'flow_chart': flow_chart
        }
        queue.put((paper_info, summary_en))
    except Exception as e:
        logger.error(f"Error processing paper: {e}")
        queue.put(f"Error: {e}")
