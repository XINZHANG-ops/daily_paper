"""
AI model configuration and abstraction layer.

Provides unified interface for AI models via local Ollama server.
"""
import os
import re
import ollama
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:32b")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.8"))
OLLAMA_NUM_CTX = int(os.getenv("OLLAMA_NUM_CTX", "32768"))


def clean_prompt(text):
    """
    Clean text by removing or replacing problematic Unicode characters.

    This handles:
    - Surrogate pairs (U+D800 to U+DFFF) that cause UTF-8 encoding errors
    - Mathematical alphanumeric symbols that may use surrogates
    - Other special characters that might cause encoding issues
    """
    if not text:
        return text

    text = re.sub(r'[\ud800-\udfff]', '', text)
    text = re.sub(r'[\U0001D400-\U0001D7FF]', '?', text)
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)

    try:
        text = text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    except Exception:
        text = text.encode('ascii', errors='ignore').decode('ascii', errors='ignore')

    return text


def model_response(prompt, model_name=None, max_tokens=8192):
    """
    Get response from Ollama model.

    Args:
        prompt: The prompt to send to the model
        model_name: Ollama model name (defaults to OLLAMA_MODEL from env)
        max_tokens: Maximum tokens in response

    Returns:
        str: Model response content
    """
    prompt = clean_prompt(prompt)
    model = model_name or OLLAMA_MODEL
    client = ollama.Client(host=OLLAMA_HOST)
    response = client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": OLLAMA_TEMPERATURE,
            "num_ctx": OLLAMA_NUM_CTX,
            "num_predict": max_tokens,
        },
    )
    return response['message']['content']
