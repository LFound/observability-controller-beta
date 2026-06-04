import os
import requests


OBSERVE_URL = os.getenv("OBSERVABILITY_API_URL")
OBSERVE_KEY = os.getenv("OBSERVABILITY_API_KEY")


if not OBSERVE_URL:
    raise RuntimeError("Set OBSERVABILITY_API_URL before running this example.")

if not OBSERVE_KEY:
    raise RuntimeError("Set OBSERVABILITY_API_KEY before running this example.")


def observe(message: str) -> dict:
    response = requests.post(
        OBSERVE_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": OBSERVE_KEY,
        },
        json={
            "message": message,
            "mode": "sufficiency_v2",
            "return_prompt": True,
        },
        timeout=20,
    )

    response.raise_for_status()
    return response.json()


def call_your_model(message: str):
    """
    Replace this function with your model call.

    Examples:
    - OpenAI
    - Claude
    - Gemini
    - Ollama
    - Mistral
    - Internal company model
    """

    raise NotImplementedError(
        "Replace call_your_model() with your chosen model provider."
    )


message = "My deployment failed."

decision = observe(message)

print("Controller decision:")
print(decision)

if decision["decision"] == "clarify":
    clarification_question = call_your_model(
        decision["clarification_prompt"]
    )

    print("\nClarification required:")
    print(clarification_question)

else:
    print("\nProceeding to model...")
    result = call_your_model(message)
    print(result)