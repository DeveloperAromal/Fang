from config.settings import *
from fang.agent.prompt.agent_prompt import PLANNER_PROMPT
from fang.utils.json_cleaner import cleanJson

from langchain_openai import ChatOpenAI
from fang.utils.logger import Logger

class Planner:
    
    def __init__(self, usr_prompt: str):
        self.usr_prompt = usr_prompt
        
        
    def _get_avail_tools():
        
        tools_list = "\n".join(
            f"- {tool['name']}: {tool['description']}"
            for tool in TOOLS_AVAILABLE
        )
        
        return tools_list
    
    
    def plan(self):
        
        prompt = PLANNER_PROMPT(self.usr_prompt, self._get_avail_tools)
        
        llm = ChatOpenAI(
            model = LLM_MODEL,
            api_key = LLM_API_KEY,
            base_url = LLM_BASE_URL
        )
        
        response = llm.invoke(prompt)
        
        try:
            result = response.content
            return cleanJson(result)
        
        except Exception:
            pass
        
        

