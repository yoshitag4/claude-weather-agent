from services.claude_service import call_claude
from services.tool_dispatcher import execute_tool
from pprint import pprint
from anthropic.types import ToolResultBlockParam


from utils.message_utils import (
    add_user_message,
    add_assistant_message,
    find_tool_use,
    find_tool_uses,
    add_tool_results_message,    
    extract_text
)


class ClaudeAgent:

    def __init__(self, tools):
        self.tools = tools
        self.messages = []        

    # Better Production Version    
    def chat(self, user_input):

        # 1. Add user message
        add_user_message(
            self.messages,
            user_input
        )


        # 2. First Claude call
        response = call_claude(
            self.messages,
            self.tools
        )
        #print("=" * 80)
        #pprint(response.content, width=120)
        #print("=" * 80)

        # 3. Store assistant response
        add_assistant_message(
            self.messages,
            response.content
        )


        # 4. Check if Claude wants a tool
        while True:

            tool_uses = find_tool_uses(response)            

            if not tool_uses:
                break

            add_tool_results_message(
                self.messages,
                tool_uses
            )
            #print (self.tools)
            response = call_claude(
                self.messages,
                self.tools
            )            

            add_assistant_message(
                self.messages,
                response.content
            )

        return extract_text(response)

    