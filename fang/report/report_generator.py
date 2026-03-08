import os
from datetime import datetime
from config.settings import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, REPORT_OUTPUT_DIR
from fang.agent.prompt.agent_prompt import REPORT_PROMPT
from fang.utils.logger import Logger
from langchain_openai import ChatOpenAI
import math
import copy


class ReportGenerator:

    def __init__(self, data: dict, target: str):
        self.data = data
        self.target = target

    def generate(self) -> str:

        Logger.info("Generating report...")
        findings = self.data.get("findings", []) if isinstance(self.data, dict) else []

        llm = ChatOpenAI(
            model=LLM_MODEL,
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL
        )

        CHUNK_SIZE = 10

        try:
            if not findings or len(findings) <= CHUNK_SIZE:
                prompt = REPORT_PROMPT(self.data, self.target)
                response = llm.invoke(prompt)
                result = response.content

            else:
                total = math.ceil(len(findings) / CHUNK_SIZE)

                first_chunk = copy.deepcopy(self.data)
                first_chunk["findings"] = findings[0:CHUNK_SIZE]

                prefix_first = (
                    f"PART 1/{total}. Produce the full report in Markdown. "
                    "Include Executive Summary, Scope & Methodology, Key Findings Summary, "
                    "and Detailed Findings ONLY for the provided findings in this part."
                )

                prompt_first = prefix_first + REPORT_PROMPT(first_chunk, self.target)
                response_first = llm.invoke(prompt_first)
                result_main = response_first.content

                fragments = []
                for i in range(1, total):
                    start = i * CHUNK_SIZE
                    end = start + CHUNK_SIZE
                    chunk_data = copy.deepcopy(self.data)
                    chunk_data["findings"] = findings[start:end]

                    prefix_part = (
                        f"PART {i+1}/{total}. Provide ONLY the markdown entries for the 'Detailed Findings' "
                        "section corresponding to the provided findings. Do NOT include Executive Summary or other sections."
                    )

                    prompt_part = prefix_part + REPORT_PROMPT(chunk_data, self.target)
                    resp = llm.invoke(prompt_part)
                    fragments.append(resp.content)

                main = result_main
                insert_after = "## Detailed Findings"
                split_after = main.split(insert_after, 1)

                if len(split_after) == 2:
                    head = split_after[0]
                    tail = split_after[1]

                    if "## Attack Surface" in tail:
                        detailed, rest = tail.split("## Attack Surface", 1)
                        combined_detailed = detailed.strip() + "\n\n" + "\n\n".join([f.strip() for f in fragments])
                        main = head + insert_after + "\n" + combined_detailed + "\n\n## Attack Surface" + rest
                    else:
                        combined_detailed = tail.strip() + "\n\n" + "\n\n".join([f.strip() for f in fragments])
                        main = head + insert_after + "\n" + combined_detailed

                result = main

            os.makedirs(REPORT_OUTPUT_DIR, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(REPORT_OUTPUT_DIR, f"report_{timestamp}.md")

            with open(filename, "w", encoding="utf-8") as f:
                f.write(result)

            Logger.success(f"Report saved → {filename}")
            return result

        except Exception as e:
            Logger.error(f"Report generation failed: {e}")
            return ""