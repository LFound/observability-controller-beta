import os
import requests
from openai import OpenAI

OBSERVE_URL = os.getenv("OBSERVABILITY_API_URL")
OBSERVE_KEY = os.getenv("OBSERVABILITY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OBSERVE_URL or not OBSERVE_KEY:
    raise RuntimeError("Set OBSERVABILITY_API_URL and OBSERVABILITY_API_KEY.")

if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY.")

client = OpenAI(api_key=OPENAI_API_KEY)


def observe(message: str) -> dict:
    response = requests.post(
        OBSERVE_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": OBSERVE_KEY,
        },
        json={"message": message},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def call_model(message: str):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=message,
    )
    return response


def run(message: str):
    decision = observe(message)

    print("Controller decision:")
    print(decision)

    if decision["decision"] == "clarify":
        print("\nClarification required before model call:")
        print(decision["clarification_question"])

        print("\nModel call: skipped")
        print("OpenAI tokens used: 0")

        return

    print("\nProceeding to model call...")
    model_response = call_model(message)

    print("\nModel answer:")
    print(model_response.output_text)

    if hasattr(model_response, "usage"):
        print("\nModel call: executed")

        if hasattr(model_response, "usage"):
            print(f"OpenAI tokens used: {model_response.usage.total_tokens}")


if __name__ == "__main__":
    run("My deployment failed.")
    print("\n" + "=" * 60 + "\n")
    run("Postgres times out during joins on 10 million rows.")
