import json
from config.settings import  LLM_BASE_URL, LLM_MODEL,LLM_API_KEY
from fang.agent.prompt.agent_prompt import ANALYZER_PROMPT
from fang.utils.logger import Logger
from fang.utils.json_cleaner import cleanJson
from fang.utils.llm_provider import LLM
from fang.memory.storage import API_KEY_CACHED


class Analyzer:

    def __init__(self, findings: dict):
        self.findings = findings

    def analyze(self) -> dict:
        Logger.info("Analyzing findings...")
        
        prompt = ANALYZER_PROMPT(self.findings)
        llm = LLM(
            model=LLM_MODEL,
            api_base_url=LLM_BASE_URL,
            api_key= API_KEY_CACHED[0] if API_KEY_CACHED else LLM_API_KEY,
        )

        response = llm.invoke(prompt, max_tokens=8192)

        if not response or not response.strip():
            Logger.error("LLM returned an empty response")
            return {}

        cleaned = cleanJson(response)

        if not cleaned:
            Logger.error(f"cleanJson returned empty. Raw response: {repr(response)}")
            return {}

        try:
            result = json.loads(cleaned)
            Logger.success("Analysis complete")
            return result
        except json.JSONDecodeError as e:
            Logger.error(f"JSON parse failed: {e} | Cleaned: {repr(cleaned)}")
            return {}