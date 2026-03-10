from fang.agent.orchestrator import Orchestrator
from fang.utils.banner import banner
from fang.utils.prompt_fn import PromptUser
from fang.agent.planner.planner import Planner
from fang.report.analyser import Analyzer
from fang.report.report_generator import ReportGenerator
from fang.utils.logger import Logger
from fang.utils.memory_filter import MemoryFilter

import json


banner()


while True:
    print("\n")
    p = PromptUser("> ").collect()
    
    if p.lower() in ("exit", "quit", "q"):
        break

    plan = json.loads(Planner(p).plan())
    target = plan.get("target_url", "")

    Logger.info(f"Target: {target}")

    Orchestrator(p, target).orchestrate(plan)
