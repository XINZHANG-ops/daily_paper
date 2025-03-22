import os
import io
import re
import yaml
import requests
from json import dumps
from loguru import logger
from httplib2 import Http
from pypdf import PdfReader
from dotenv import load_dotenv
from datetime import datetime, timezone
from geotab_genai.genai_gateway_client import GenaiGatewayClient


load_dotenv()
SPACE_ID = os.getenv("SPACE_ID")
KEY = os.getenv("KEY")


# summary_test = "The summary"
# test_questions = [
#         {
#             'question': 'What is the main contribution of this paper?',
#             'choices': ['Option A', 'Option B', 'Option C', 'Option D'],
#             'answer': 'Option A'
#         },
#         {
#             'question': 'Which dataset was used in this study?',
#             'choices': ['Dataset X', 'Dataset Y', 'Dataset Z'],
#             'answer': 'Dataset Y'
#         }
#     ]

# test_questions = [
#         {
#             'question': 'What is the main focus?'*10,
#             'choices': ['A'*100, 'B'*100, 'C'*100],
#             'answer': 'B'*100
#         },
#         {
#             'question': 'Which method is used?'*10,
#             'choices': ['X'*100, 'Y'*100, 'Z'*100],
#             'answer': 'Y'*100
#         },
#         {
#             'question': 'Which method is used?'*10,
#             'choices': ['X'*100, 'Y'*100, 'Z'*100],
#             'answer': 'Y'*100
#         }
#     ]

# hugging face utils
def fetch_huggingface_papers(limit=100):
    """
    Fetches papers from the Hugging Face API endpoint.
    """
    API_URL = "https://huggingface.co/api/daily_papers"
    
    try:
        response = requests.get(f"{API_URL}?limit={limit}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching papers: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def process_papers(papers, sort_method="hot"):
    """
    Process and sort the papers based on the specified method.
    """
    processed_papers = []
    
    for paper in papers:
        title = paper.get('title', 'No title')
        paper_id = paper.get('paper', {}).get('id', '')
        url = f"https://huggingface.co/papers/{paper_id}"
        authors = [author.get('name', '') for author in paper.get('paper', {}).get('authors', [])]
        upvotes = paper.get('paper', {}).get('upvotes', 0)
        comments = paper.get('numComments', 0)
        published_at_str = paper.get('publishedAt', datetime.now(timezone.utc).isoformat())
        
        try:
            published_time = datetime.fromisoformat(published_at_str.replace('Z', '+00:00'))
        except ValueError:
            published_time = datetime.now(timezone.utc)
            
        time_diff = datetime.now(timezone.utc) - published_time
        days_ago = time_diff.days
        
        if sort_method == "hot":
            time_diff_hours = time_diff.total_seconds() / 3600
            score = upvotes / ((time_diff_hours + 2) ** 1.5)
        elif sort_method == "rising":
            time_diff_hours = time_diff.total_seconds() / 3600
            score = upvotes / (time_diff_hours + 1)
        else:  # "new" - just use published time
            score = published_time.timestamp()
            
        processed_papers.append({
            'title': title,
            'url': url,
            'paper_id': paper_id,
            'authors': authors,
            'upvotes': upvotes,
            'comments': comments,
            'published_at': published_time.isoformat(),
            'days_ago': days_ago,
            'score': score
        })
    
    if sort_method == "new":
        return sorted(processed_papers, key=lambda x: x['published_at'], reverse=True)
    else:  # "hot" or "rising"
        return sorted(processed_papers, key=lambda x: x['score'], reverse=True)


def get_huggingface_papers(sort_method="hot", limit=100):
    """
    Main function to fetch and process HuggingFace papers.
    """
    raw_papers = fetch_huggingface_papers(limit)
    if raw_papers:
        return process_papers(raw_papers, sort_method)
    return []


# arxiv utils
def extract_arxiv_id(paper_info):
    """Extract the arXiv ID from paper information."""
    if isinstance(paper_info, dict):
        paper_id = paper_info.get('paper_id')        
        if not paper_id and 'url' in paper_info:
            url = paper_info['url']
            # Extract ID from URLs like https://huggingface.co/papers/2502.18417
            match = re.search(r'papers/(\d+\.\d+)', url)
            if match:
                paper_id = match.group(1)
    else:
        paper_id = paper_info
    
    # Verify it looks like an arXiv ID (YYMM.number format)
    if paper_id and re.match(r'\d{4}\.\d+', paper_id):
        return paper_id
    return None


def get_arxiv_pdf_url(paper_info):
    """Get the PDF URL for an arXiv paper."""
    arxiv_id = extract_arxiv_id(paper_info)
    if not arxiv_id:
        return None
    return f"http://arxiv.org/pdf/{arxiv_id}"


def download_paper_text(paper_info):
    """Download and extract text from a paper PDF."""
    pdf_url = get_arxiv_pdf_url(paper_info)
    if not pdf_url:
        return {
            "success": False,
            "message": "Not an arXiv paper or invalid paper information",
            "pdf_url": None,
            "text": None,
            "pages": 0
        }
    
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
        
        pdf_file = io.BytesIO(response.content)
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        
        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n\n"
        
        return {
            "success": True,
            "message": "Successfully downloaded and extracted text",
            "pdf_url": pdf_url,
            "text": text,
            "pages": num_pages
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Error downloading PDF: {str(e)}",
            "pdf_url": pdf_url,
            "text": None,
            "pages": 0
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error processing PDF: {str(e)}",
            "pdf_url": pdf_url,
            "text": None,
            "pages": 0
        }



# google chat utils
def format_text(content):
    import re
    
    content_lines = content.split('\n')
    content_widgets = []
    
    def replace_bold(line):
        return re.sub(r'\*\*(.*?)\*\*', 
                      r'<font color="#ff0000"><b>\1</b></font>', 
                      line)
    
    for line in content_lines:
        line = line.strip()
        if not line:
            continue
        
        formatted_line = replace_bold(line)
        
        if formatted_line.startswith('- ') or formatted_line.startswith('* '):
            formatted_line = f"• {formatted_line[2:]}"
        
        content_widgets.append({
            "textParagraph": {
                "text": formatted_line
            }
        })
    
    return content_widgets


def create_article_message(articles):
    sections = []
    
    for idx, article in enumerate(articles):
        title = article.get('title', 'No Title')
        published_at = article.get('published_at', 'No Date')
        url = article.get('url', '#')
        content = article.get('content', 'No Content')
        
        sections.append({
            "header": f"Paper {idx+1}",
            "widgets": [
                {
                    "decoratedText": {
                        "text": title,
                        "startIcon": {
                            "knownIcon": "BOOKMARK"
                        },
                        "wrapText": True
                    }
                },
                {
                    "textParagraph": {
                        "text": f"<b>Published:</b> {published_at}"
                    }
                },
                {
                    "textParagraph": {
                        "text": f"<b>Link:</b> <a href=\"{url}\">{url}</a>"
                    }
                },
                {
                    "divider": {}
                }
            ]
        })

        content_widgets = format_text(content=content)
        
        sections.append({
            "widgets": content_widgets
        })
        
        if idx < len(articles) - 1:
            sections.append({
                "widgets": [
                    {
                        "textParagraph": {
                            "text": "<font color=\"#34a853\">--------------------------- END OF SUMMARY ---------------------------</font>"
                        }
                    }
                ]
            })
    
    app_message = {
        "cardsV2": [{
            "cardId": "article-collection",
            "card": {
                "header": {
                    "title": "Daily Papers",
                    "subtitle": f"{len(articles)} paper(s) for today"
                },
                "sections": sections
            }
        }]
    }
    
    return app_message


def send_articles(articles, thread_id):
    url = f"https://chat.googleapis.com/v1/spaces/{SPACE_ID}/messages?key={KEY}&messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD"
    
    app_message = create_article_message(articles)
    
    app_message["thread"] = {"threadKey": thread_id}
    
    # Send the message
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    return response

def start_thread(current_date, additional_content, thread_key_value):
    """Google Chat incoming webhook that starts or replies to a message thread."""
    url = f"https://chat.googleapis.com/v1/spaces/{SPACE_ID}/messages?key={KEY}&messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD"
    reminder = """Treat it as a tool for selecting papers rather than for fully understanding them. It will help you understand the standing of a paper in the field, and once you’ve chosen one, you’ll read it more efficiently with a questioning mindset."""

    # Construct the correct GitHub Pages subpage URL
    link = f"https://xinzhang-ops.github.io/daily_paper/{current_date}.html"
    link = f"""<a href="{link}" target="_blank"> link </a>"""

    # Create the structured message with sections and widgets
    app_message = {
        "cardsV2": [{
            "cardId": "daily-papers-header",
            "card": {
                "header": {
                    "title": f"{current_date} Papers",
                    "subtitle": "Daily Paper Updates"
                },
                "sections": [
                    {
                        "widgets": [
                            {"textParagraph": {"text": reminder}}
                        ]
                    },
                    {
                        "widgets": [
                            {"decoratedText": {
                                    "text": 
                                    f"<font color=\"#4D516D\"><b>{additional_content}</b></font>", 
                                    "startIcon": {"knownIcon": "STAR"}, "topLabel": "Quote of the day:", "wrapText": True
                                }
                            }
                        ]
                    },
                    {
                        "widgets": [
                            {"textParagraph": {"text": f"""<b>If you prefer link:</b> {link}"""}}
                        ]
                    }
                ]
            }
        }],
        "thread": {"threadKey": thread_key_value}
    }

    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    return response

provider = 'anthropics'
model = 'claude-3-5-sonnet-v2'
client_llm = GenaiGatewayClient(
    api_key=os.getenv("GENAI_GATEWAY_API_KEY"),
    env="staging",
    jurisdiction="us",
    temperature=1,
    provider='anthropics',
    chat_model='claude-3-5-sonnet-v2',
)

# provider = 'vertex-ai'
# model = 'gemini-2.0-pro'
# client_llm = GenaiGatewayClient(
#     api_key=os.getenv("GENAI_GATEWAY_API_KEY"),
#     env="staging",
#     jurisdiction="us",
#     temperature=0.5,
#     provider=provider,
#     chat_model=model,
# )

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
def summary_paper(paper_title, paper_content):
    prompt = PROMPT.format(
        title=paper_title,
        content=paper_content
    )
    logger.debug(f"Prompt length: {len(prompt.split(' '))}")

    summary = client_llm.create_message(messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
        max_tokens=1024,
        provider=provider,
        model=model,
        version=None
    )['message']['content']
    return summary

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
It can about the problem solved of the paper, the method of the paper or impact of the paper or literally anything.
Each question should has only 3 options, for each question you should generate the question, options and the correct answer.

Follow exactly the format below for your outputs:

- question: hello
  option1: option1 statement
  option2: option2 statement
  option3: option3 statement
  answer: option1 or option2 or option3

- question: hello
  option1: option1 statement
  option2: option2 statement
  option3: option3 statement
  answer: option1 or option2 or option3

- question: hello
  option1: option1 statement
  option2: option2 statement
  option3: option3 statement
  answer: option1 or option2 or option3

Notice you need to generate 3 questions as shown in template.
Now output your the questions and nothing else:
"""

def create_question(paper_title, paper_content, summary):
    prompt = QUESTION_PROMPT.format(
        title=paper_title,
        content=paper_content,
        summary=summary
    )
    questions_content = client_llm.create_message(messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
        max_tokens=1024,
        provider=provider,
        model=model,
        version=None
    )['message']['content']
    questions = yaml.safe_load(questions_content)
    return questions


def find_not_proposed_papers(
        grab_papers: list[dict], 
        current_paper_list: list[str], 
    ) -> tuple[list[dict], list[str]]:
    """Grab n new papers."""
    new_papers = []
    new_titles = []
    for paper_data in grab_papers:
        paper_title = paper_data['title']
        if paper_title in current_paper_list:
            continue
        else:
            new_papers.append(paper_data)
            new_titles.append(paper_title)
    return new_papers, current_paper_list + new_titles
        

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


BASE_URL = "https://api.quotable.io"

def fetch_data(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        # Disable SSL verification
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def process_paper(paper, queue, max_paper_length):
    """Run paper processing in a thread and put the result in a queue."""
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
        
        paper_info = {
            'title': title,
            'published_at': published_at,
            'url': paper_url,
            'content': summary,
            'questions': test_questions
        }
        queue.put((paper_info, summary))
    except Exception as e:
        queue.put(f"Error: {e}")


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
