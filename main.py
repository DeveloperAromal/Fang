from fang.agent.orchestrator import Orchestrator
from fang.utils.banner import banner
from fang.utils.ip_data import IPData
from fang.utils.prompt_fn import PromptUser
from fang.agent.planner.planner import Planner
from fang.utils.logger import Logger
import json


banner()


while True:

    p = PromptUser("> ").collect()
    
    if p.lower() in ("exit", "quit", "q"):
        break

    plan = json.loads(Planner(p).plan())

    target = plan["target_url"]
    Logger.result("recon", Orchestrator(p, target).orchestrate(plan))
    