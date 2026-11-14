"""Functions for creating and updating conversation history."""

def create_messages(user_prompt: str) -> list[dict]:
    """Create a fresh conversation for one user request."""
    return [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant with access to a calculator and web search. "
                "Use web_search when current or externally sourced information is needed. "
                "Use calculator for exact arithmetic. For multi-step tasks, inspect tool "
                "results before continuing. Do not invent search results. If a tool fails, "
                "explain that clearly. Include source URLs when using web search."
            ),
        },
        {"role": "user", "content": user_prompt},
    ]


def append_assistant_message(messages: list[dict], assistant_message) -> None:
    """Preserve the assistant response, including structured tool calls."""
    messages.append(assistant_message)


def append_tool_result(
    messages: list[dict],
    tool_name: str,
    result: str,
) -> None:
    """Append a tool response so the model can use it on the next iteration."""
    messages.append(
        {
            "role": "tool",
            "tool_name": tool_name,
            "content": str(result),
        }
    )
