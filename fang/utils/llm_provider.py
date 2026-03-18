import requests


class LLM:

    def __init__(self, model: str, api_base_url: str, api_key: str):
        self.model = model
        self.api_base_url = api_base_url
        self.api_key = api_key

    def invoke(
        self,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
    ) -> str:
      
        url = (
            f"{self.api_base_url}/models/{self.model}"
            f":generateContent?key={self.api_key}"
        )

        payload: dict = {
            "contents": [
                {"role": "user", "parts": [{"text": prompt}]}
            ],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
            },
        }

        if system_prompt:
            payload["system_instruction"] = {
                "parts": [{"text": system_prompt}]
            }

        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()

        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]