"""
AI model configuration and abstraction layer.

Provides unified interface for multiple AI models including Claude and Gemini variants.
"""
import os
import re
from geotab_genai.genai_gateway_client import GenaiGatewayClient


claude35_sonnet_v2 = GenaiGatewayClient(
    api_key=os.getenv("GENAI_GATEWAY_API_KEY"),
    env="staging",
    jurisdiction="us",
    temperature=0.8,
    provider='anthropics',
    chat_model='claude-3-5-sonnet-v2',
    max_tokens=8192,
    safety_filtering='off'
)


claude4_sonnet = GenaiGatewayClient(
    api_key=os.getenv("GENAI_GATEWAY_API_KEY"),
    env="staging",
    jurisdiction="us",
    temperature=0.8,
    provider='anthropics',
    chat_model='claude-sonnet-4',
    max_tokens=8192,
    safety_filtering='off'
)

claude4_opus = GenaiGatewayClient(
    api_key=os.getenv("GENAI_GATEWAY_API_KEY"),
    env="staging",
    jurisdiction="us",
    temperature=0.8,
    provider='anthropics',
    chat_model='claude-opus-4',
    max_tokens=8192,
    safety_filtering='off'
)


claude37_sonnet = GenaiGatewayClient(
    api_key=os.getenv("GENAI_GATEWAY_API_KEY"),
    env="staging",
    jurisdiction="us",
    temperature=0.8,
    provider='anthropics',
    chat_model='claude-3-7-sonnet',
    max_tokens=8192,
    safety_filtering='off'
)


model_map = {
    'claude4': claude4_sonnet,
    'claude35': claude35_sonnet_v2,
    'claude37': claude37_sonnet,
}


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

    # Remove surrogate pairs (U+D800-U+DFFF)
    # These are invalid in UTF-8 and cause encoding errors
    text = re.sub(r'[\ud800-\udfff]', '', text)

    # Replace common mathematical symbols that might be problematic
    # Mathematical bold/italic letters often cause issues
    text = re.sub(r'[\U0001D400-\U0001D7FF]', '?', text)

    # Remove other problematic Unicode ranges
    # Control characters and other special ranges
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)

    # Ensure the text is properly encoded/decoded
    try:
        # Try to encode and decode to ensure valid UTF-8
        text = text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    except Exception:
        # If all else fails, use ASCII-safe representation
        text = text.encode('ascii', errors='ignore').decode('ascii', errors='ignore')

    return text


def model_response(prompt, model_name, max_tokens=8192):
    """
    Get response from specified AI model.

    Args:
        prompt: The prompt to send to the model
        model_name: Name of the model (key in model_map)
        max_tokens: Maximum tokens in response

    Returns:
        str: Model response content
    """
    # Clean the prompt to remove problematic Unicode characters
    prompt = clean_prompt(prompt)

    model = model_map[model_name]
    version = None
    response = model.create_message(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        provider=model._provider,
        model=model._chat_model,
        version=version,

    )['message']['content']
    return response


# import requests

# SERVER_IP = "10.0.0.174"


# def model_response(prompt, model_name, max_tokens=8192):
#     response = requests.post(
#         f"http://{SERVER_IP}:5000/chat",
#         json={"message": prompt, "model":model_name, "max_tokens": max_tokens}
#     )
#     return response.json()["response"]
