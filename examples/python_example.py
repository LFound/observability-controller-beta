import os
import requests

API_URL = os.getenv("OBSERVABILITY_API_URL")
API_KEY = os.getenv("OBSERVABILITY_API_KEY")

response = requests.post(
    API_URL,
    headers={
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
    },
    json={
        "message": "My deployment failed."
    },
)

print(response.json())
