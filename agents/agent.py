
# Maintain conversation history
chat_history = []


def chat(user_input: str):

    chat_history.append({
        "role": "user",
        "content": user_input
    })

    result = agent.invoke({
        "messages": chat_history
    })

    # Preserve the entire returned message history,
    # including AI messages and tool results.
    chat_history[:] = result["messages"]

    return result["messages"][-1].content
