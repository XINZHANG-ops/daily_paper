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

gemini_20_pro = GenaiGatewayClient(
    api_key=os.getenv("GENAI_GATEWAY_API_KEY"),
    env="staging",
    jurisdiction="us",
    temperature=0.8,
    provider='vertex-ai',
    chat_model='gemini-2.0-pro',
    max_tokens=8192,
    safety_filtering='off'
)

gemini_25_pro = GenaiGatewayClient(
    api_key=os.getenv("GENAI_GATEWAY_API_KEY"),
    env="staging",
    jurisdiction="us",
    temperature=0.8,
    provider='vertex-ai',
    chat_model='gemini-2.5-pro',
    max_tokens=8192,
    safety_filtering='off'
)

gemini_25_flash = GenaiGatewayClient(
    api_key=os.getenv("GENAI_GATEWAY_API_KEY"),
    env="staging",
    jurisdiction="us",
    temperature=0.8,
    provider='vertex-ai',
    chat_model='gemini-2.5-flash',
    max_tokens=8192,
    safety_filtering='off'
)


model_map = {
    'claude35': claude35_sonnet_v2,
    'claude37': claude37_sonnet,
    'gemini_20_pro': gemini_20_pro,
    'gemini_25_pro': gemini_25_pro,
    '2.5 flash': gemini_25_flash,
}


def model_response(prompt, model_name, max_tokens=8192):
    model = model_map[model_name]
    version = None
    if model_name == 'gemini_20_flash':
        version = '001'
    if model_name == 'gemini_25_pro':
        version = 'exp-03-25'
    if model_name == '2.5 flash':
        version = 'preview-04-17'
    response = model.create_message(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        provider=model._provider,
        model=model._chat_model,
        version=version,

    )['message']['content']
    return response