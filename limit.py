import requests

api_key = "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"
url = "https://openrouter.ai/api/v1/auth/key"

headers = {
    "Authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("API Response:", response.json())
else:
    print("Error:", response.status_code, response.text)
