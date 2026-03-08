import re

def cleanJson(raw: str) -> str:
    cleaned = re.sub(r"```(?:json)?\s*([\s\S]*?)```", r"\1", raw.strip())
    return cleaned.strip()