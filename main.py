import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

def generate_content(client: OpenAI, messages: list) -> None:
    return client.chat.completions.create(
        model="openrouter/free",
        messages= messages
    )

def main() -> None:
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
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
        {"role": "user", "content": args.user_prompt},
    ]

    response = generate_content(client, messages)

    if response.usage is None:
        raise RuntimeError("Usage proterty is None.")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}")
    print("Response:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()