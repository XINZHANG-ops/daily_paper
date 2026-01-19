"""
Google Chat Integration Utilities

This module provides functions for formatting messages and sending notifications
to Google Chat spaces using webhooks. It handles message formatting, card creation,
and thread management for daily paper notifications.
"""

import os
import re
from json import dumps
from httplib2 import Http
from dotenv import load_dotenv


load_dotenv()
SPACE_ID = os.getenv("SPACE_ID")
KEY = os.getenv("KEY")


def format_text(content):
    """
    Format text content for Google Chat cards, converting markdown to HTML.

    This function processes markdown-like content and converts it into Google Chat
    widget format with HTML styling. It handles bold text and bullet points.

    Args:
        content (str): The content to format, potentially containing markdown

    Returns:
        list: A list of Google Chat text paragraph widgets
    """
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
    """
    Create a Google Chat card message containing multiple article summaries.

    This function formats a list of articles into a structured Google Chat card
    with sections for each article, including title, publication date, URL, and content.

    Args:
        articles (list): List of article dictionaries containing 'title', 'published_at',
                        'url', and 'content' keys

    Returns:
        dict: A Google Chat cardsV2 message structure
    """
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
    """
    Send articles to a Google Chat space in a specific thread.

    Args:
        articles (list): List of article dictionaries to send
        thread_id (str): The thread key to reply to or create

    Returns:
        tuple: HTTP response from the Google Chat API
    """
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
    """
    Start a new Google Chat thread or reply to an existing one with daily paper header.

    This function creates the initial message for daily papers, including a reminder,
    quote of the day, and link to the full paper list.

    Args:
        current_date (str): The date string in YYYY-MM-DD format
        additional_content (str): Quote or additional message to include
        thread_key_value (str): The thread key for message threading

    Returns:
        tuple: HTTP response from the Google Chat API
    """
    url = f"https://chat.googleapis.com/v1/spaces/{SPACE_ID}/messages?key={KEY}&messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD"
    reminder = """Treat it as a tool for selecting papers rather than for fully understanding them. It will help you understand the standing of a paper in the field, and once you've chosen one, you'll read it more efficiently with a questioning mindset."""

    # Construct the correct GitHub Pages subpage URL
    link = f"https://xinzhang-ops.github.io/daily_paper/dailies/pages/{current_date}.html"
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
