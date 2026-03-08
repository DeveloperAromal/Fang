from .planner.planner import Planner
from config.settings import TOOLS_AVAILABLE
from fang.memory.storage import STORAGE
from fang.utils.logger import Logger
from typing import List
import traceback


TOOLS_BY_NAME = {tool["name"]: tool for tool in TOOLS_AVAILABLE}

class Orchestrator:
    
    def __init__(self, usr_prompt: str, target: str):
        self.usr_prompt = usr_prompt
        self.target = target
        
    
    def _plan(self):
        return Planner(self.usr_prompt).plan().json()
    
    
    def _resolve_order(self, selected: List[str]) -> List[str]:
        
        ordered = list(selected)
        
        for tool_name in selected:
            
            tool = TOOLS_BY_NAME.get(tool_name, {})
            dep = tool.get("depends_on")
            
            if dep and dep in ordered:
                
                dep_idx = ordered.index(dep)
                tool_idx = ordered.index(tool_name)
                
                if tool_idx < dep_idx:
                    ordered.remove(tool_name)
                    ordered.insert(dep_idx + 1, tool_name)
                    
        return ordered
        
    
    def _run_tool(self, tools: List[str]) -> None:
        
        tools = self._resolve_order(tools)
            
        
        for tool_name in tools:
            tool = TOOLS_BY_NAME.get(tool_name)
            
            if not tool:
                continue
            
                Logger.info(f"{tool_name}...")
            try:
                result = tool["executor"](self.target, STORAGE)

                STORAGE[tool["storage_key"]] = result
                Logger.success(f"{tool_name} completed")

            except Exception as e:
                Logger.error(f"{tool_name} failed: {e}")
                Logger.error(traceback.format_exc())
    
    
    def orchestrate(self,  plan: dict):
        
        self._run_tool(plan.get("selected_tools", []))
        
        Logger.info("Recon complete. Findings:")
        
        for key in STORAGE:
              Logger.result(key, STORAGE[key])

        return {
            "target":    self.target,
            "objective": plan.get("objective", ""),
            "findings":  dict(STORAGE),
        }
    
    
    