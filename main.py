"""Entry point and agentic orchestration loop for local Ollama + Mistral."""
import time
import logging

from ollama import chat

from messages import create_messages, append_assistant_message, append_tool_result
from schema.tool_schemas import TOOLS
from tools.init import execute_tool

# MODEL = "gemma3:1b"  # Replace with the exact tag shown by `ollama list`.
MODEL = "qwen2.5:3b"# MODEL = "mistral"  # Replace with the exact tag shown by `ollama list`.
MAX_ITERATIONS = 20

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

def run_agent(user_prompt: str, messages: list | None = None) -> str:
    """Run one task; optionally continue using an existing conversation history."""

    start_time = time.perf_counter()

    try:
        if messages is None:
            messages = create_messages(user_prompt)
        else:
            messages.append({"role": "user", "content": user_prompt})

        for iteration in range(1, MAX_ITERATIONS + 1):
            logger.info("Agent iteration %s/%s", iteration, MAX_ITERATIONS)

            response = chat(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                stream=False,
            )

            assistant_message = response.message
            append_assistant_message(messages, assistant_message)

            tool_calls = assistant_message.tool_calls or []

            if not tool_calls:
                final_answer = assistant_message.content or ""

                if not final_answer.strip():
                    raise RuntimeError(
                        "Model returned neither tool calls nor a final text response."
                    )

                logger.info("Assistant completed the task.")
                return final_answer

            for tool_call in tool_calls:
                name = tool_call.function.name
                arguments = tool_call.function.arguments or {}

                logger.info(
                    "Tool requested: %s | Arguments: %s",
                    name,
                    arguments,
                )

                result = execute_tool(name, arguments)
                logger.info("Tool result: %s", result[:500])

                append_tool_result(messages, name, result)

        logger.warning(
            "Safety iteration cap (%s) reached. Stopping the agent.",
            MAX_ITERATIONS,
        )

        return (
            "The agent stopped because it reached its maximum iteration limit. "
            "Please try a simpler or more specific request."
        )

    finally:
        elapsed_time = time.perf_counter() - start_time

        logger.info(
            "Total agent execution time: %.2f seconds (%.3f ms)",
            elapsed_time,
            elapsed_time * 1000,
        )

def main() -> None:
    """Interactive terminal trigger."""
    print("Local Mistral Agent")
    print("Tools: calculator, web_search")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not user_input:
            continue

        try:
            answer = run_agent(user_input)
            print(f"\nAssistant: {answer}\n")
        except Exception as error:
            logger.exception("Agent failed")
            print(f"\nAgent error: {error}\n")


if __name__ == "__main__":
    main()
