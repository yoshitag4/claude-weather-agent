
from config.anthropic_config import client, MODEL
from prompts.system_prompt import SYSTEM_PROMPT

def call_claude(messages, tools):

    return client.messages.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        system=SYSTEM_PROMPT,
        max_tokens=1000
    )