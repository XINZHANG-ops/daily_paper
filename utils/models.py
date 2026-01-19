"""
AI model configuration and abstraction layer.

Provides unified interface for multiple AI models including Claude and Gemini variants.
"""
import os
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
    'claude4': claude4_opus,
    'claude35': claude35_sonnet_v2,
    'claude37': claude37_sonnet,
}


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
