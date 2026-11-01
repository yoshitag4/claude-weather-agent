from agent.claude_agent import ClaudeAgent
from schemas import ALL_TOOLS


def main():

    agent = ClaudeAgent(
        tools=ALL_TOOLS
    )


    print("Weather Agent Started 🌤️")
    print("Ask me weather questions.")
    print("Type 'exit' to quit.\n")


    while True:

        user_input = input("You: ")


        if user_input.lower() in [
            "exit",
            "quit",
            "bye"
        ]:
            print("Goodbye!")
            break

        response = agent.chat(            
            user_input
        )


        print("\nAssistant:")
        print(response)
        print("-" * 50)



if __name__ == "__main__":
    main()