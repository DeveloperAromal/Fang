import json
from config.settings import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
from fang.agent.prompt.agent_prompt import ANALYZER_PROMPT
from fang.utils.logger import Logger
from fang.utils.json_cleaner import cleanJson
from langchain_openai import ChatOpenAI


class Analyzer:

    def __init__(self, findings: dict):
        self.findings = findings

    def analyze(self) -> dict:

        Logger.info("Analyzing findings...")

        prompt = ANALYZER_PROMPT(self.findings)

        llm = ChatOpenAI(
            model=LLM_MODEL,
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL
        )

        response = llm.invoke(prompt)

        try:
            result = json.loads(cleanJson(response.content))
            Logger.success("Analysis complete")
            return result

        except Exception as e:
            Logger.error(f"Analysis failed: {e}")
            return {}