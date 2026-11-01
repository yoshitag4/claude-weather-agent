from services.tool_dispatcher import TOOL_REGISTRY
from anthropic.types import ToolResultBlockParam


def add_user_message(messages, text):
    user_message = {
        "role": "user",
        "content": text
    }
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {
        "role": "assistant",
        "content": text
    }
    messages.append(assistant_message)

# This works for sinlgle message tool use
def add_tool_result_message(messages, tool_use_id, result):
    messages.append(
        {
            "role": "user",
            "content": [
                ToolResultBlockParam(
                    type="tool_result",
                    tool_use_id=tool_use_id,
                    content=result
                )
            ]
        }
    )    

# this works for multiple tool uses
def add_tool_results_message(messages, tool_uses):

    tool_results = []
    for tool_use in tool_uses:
        result = execute_tool(tool_use)
        tool_results.append(
            ToolResultBlockParam(
                type="tool_result",
                tool_use_id=tool_use.id,
                content=result
            )
        )
    messages.append(
        {
            "role": "user",
            "content": tool_results
        }
    )


def extract_text(response):

    texts = []

    for block in response.content:
        if block.type == "text":
            texts.append(block.text)

    return "\n".join(texts)

def find_tool_use(response):
    """
    Returns the first ToolUseBlock from Claude's response.
    Returns None if no tool was requested.
    """

    for block in response.content:
        if block.type == "tool_use":
            return block

    return None

def find_tool_uses(response):
    
    tool_uses = []
    for block in response.content:
        if block.type == "tool_use":
            tool_uses.append(block)

    return tool_uses

def execute_tool(tool_use):
    """
    Executes the requested tool and returns the result.
    """

    tool = TOOL_REGISTRY.get(tool_use.name)

    if tool is None:
        raise ValueError(
            f"Unknown tool: {tool_use.name}"
        )

    return tool(**tool_use.input)
