from fang.agent.orchestrator import Orchestrator
from fang.utils.banner import banner
from fang.utils.prompt_fn import PromptUser
from fang.agent.planner.planner import Planner
from fang.utils.logger import Logger

from fang.utils.config_helpers import ConfigHelper

import json


banner()

config = ConfigHelper()

while True:
    config.check()

    print()

    p = PromptUser("[#Fang] > ").collect()

    if p.lower() in ("exit", "quit", "q"):
        break

    plan = json.loads(Planner(p).plan())
    target = plan.get("target_url", "")

    Logger.info(f"Target: {target}")

    Orchestrator(p, target).orchestrate(plan)