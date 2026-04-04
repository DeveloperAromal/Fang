from config.settings import LLM_MODEL, LLM_BASE_URL, TOOLS_AVAILABLE, LLM_API_KEY
from fang.agent.prompt.agent_prompt import PLANNER_PROMPT
from fang.utils.json_cleaner import cleanJson
from fang.utils.llm_provider import LLM
from fang.memory.storage import API_KEY_CACHED

class Planner:

    def __init__(self, usr_prompt: str):
        self.usr_prompt = usr_prompt


    @staticmethod
    def _get_avail_tools() -> str:
        tools_list = "\n".join(
            f"- {tool['name']}: {tool['description']}"
            for tool in TOOLS_AVAILABLE
        )
        return tools_list


    def plan(self):
        prompt = PLANNER_PROMPT(self.usr_prompt, self._get_avail_tools())

        llm = LLM(
            model=LLM_MODEL,
            api_base_url=LLM_BASE_URL,
            api_key= API_KEY_CACHED[0] if API_KEY_CACHED else LLM_API_KEY,
        )

        response = llm.invoke(prompt)
        try:
            return cleanJson(response)
        except Exception:
            pass