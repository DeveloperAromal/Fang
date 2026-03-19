import re

def cleanJson(raw: str) -> str:
    if not raw or not raw.strip():
        return ""

    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if fence_match:
        return fence_match.group(1).strip()

    json_match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", raw)
    if json_match:
        return json_match.group(1).strip()

    return ""