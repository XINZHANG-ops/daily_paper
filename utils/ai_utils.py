"""
AI Generation Utilities

This module provides functions for AI-powered content generation including paper summaries,
question creation, flowchart generation, and text parsing. It uses various AI models to
analyze academic papers and create structured outputs.
"""

import re
import json
from loguru import logger
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


def summary_paper(paper_title, paper_content):
    """
    Generate a structured summary of an academic paper.

    This function uses an AI model to analyze a paper and provide a concise summary
    covering five key aspects: topic, previous research, problem, methods, and results.

    Args:
        paper_title (str): The title of the paper
        paper_content (str): The full text content of the paper

    Returns:
        str: A formatted summary with five categorized sections
    """
    logger.debug(f'Creating summary for "{paper_title}"')
    prompt = PROMPT.format(
        title=paper_title,
        content=paper_content
    )
    logger.debug(f"Prompt length: {len(prompt.split(' '))}")

    summary = model_response(
        prompt,
        'claude4',
        max_tokens=8000

    )
    return summary


def create_question(paper_title, paper_content, summary):
    """
    Generate quiz questions about an academic paper.

    Creates three multiple-choice questions based on the paper content and summary,
    testing understanding of key concepts, methods, or findings.

    Args:
        paper_title (str): The title of the paper
        paper_content (str): The full text content of the paper
        summary (str): A summary of the paper

    Returns:
        dict: A dictionary containing three questions with options and answers
    """
    logger.debug(f'Creating question for "{paper_title}"')
    prompt = QUESTION_PROMPT.format(
        title = paper_title,
        content = paper_content,
        summary = summary,
    ) + QUESTION_FORMAT

    questions_content = model_response(
        prompt,
        'claude4',
        max_tokens=8000

    )
    logger.debug(questions_content)
    questions = parse_output(questions_content)
    return questions


def create_flow_chart(paper_title, paper_content):
    """
    Generate an SVG flowchart visualizing the paper's methodology.

    Creates a visual flowchart representation of the paper's workflow and methods
    in SVG format.

    Args:
        paper_title (str): The title of the paper
        paper_content (str): The full text content of the paper

    Returns:
        str: SVG markup representing the flowchart
    """
    logger.debug(f'Creating flow chart for "{paper_title}"')
    prompt = FLOW_CHART_PROMPT.format(
        title=paper_title,
        article_content=paper_content
    )
    flow_chart = model_response(
        prompt,
        'claude4',
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


def process_paper(paper, queue, max_paper_length):
    """
    Process a single paper: download, summarize, create quiz, generate flowchart.

    This function runs in a thread and puts the result in a queue.

    Args:
        paper (dict): Paper information from HuggingFace
        queue (Queue): Thread-safe queue to store results
        max_paper_length (int): Maximum word count for papers
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

        summary = summary_paper(title, content)
        questions = create_question(
            paper_title=title,
            paper_content=content,
            summary=summary
        )
        flow_chart = create_flow_chart(
            paper_title=title,
            paper_content=content
        )

        paper_info = {
            'title': title,
            'published_at': published_at,
            'url': paper_url,
            'content': summary,
            'questions': questions,
            'flow_chart': flow_chart
        }
        queue.put((paper_info, summary))
    except Exception as e:
        logger.error(f"Error processing paper: {e}")
        queue.put(f"Error: {e}")
