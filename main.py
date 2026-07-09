import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from config import MAX_ITERS
from prompts import system_prompt
from call_function import available_functions, call_function

def generate_content(client: OpenAI, messages: list, args: argparse.Namespace) -> str | None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages= messages,
        temperature=0,
        tools=available_functions,
    )

    if response.usage is None:
        raise RuntimeError("Usage property is None.")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    
    message = response.choices[0].message
    messages.append(message)
    if not message.tool_calls:
        return message.content
    
    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result = call_function(tool_call, verbose= args.verbose)
        if result.get("content") is None:
            raise RuntimeError(f"Empty function response for  '{tool_call.function.name}'")
        if args.verbose:
            print(f"Function result: {result['content']}")
        messages.append(result)
    
    return None

def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("API key not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(MAX_ITERS):
        try:
            final_response = generate_content(client, messages, args)
            if final_response is not None:
                print(f"Final response: {final_response}")
                return
        except Exception as e:
            print(f"Error occurred: {e}")
    print("Maximum attempts reached. Exiting.")
    sys.exit(1)

if __name__ == "__main__":
    main()