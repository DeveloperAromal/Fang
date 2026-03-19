from config.settings import LLM_MODEL, LLM_BASE_URL, TOOLS_AVAILABLE, get_api_key
from fang.agent.prompt.agent_prompt import PLANNER_PROMPT
from fang.utils.json_cleaner import cleanJson
from fang.utils.llm_provider import LLM


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
            api_key=get_api_key(),     
        )

        response = llm.invoke(prompt)

        try:
            return cleanJson(response)
        except Exception:
            pass