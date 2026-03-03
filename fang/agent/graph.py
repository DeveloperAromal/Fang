from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .tools import (
    scan_port,
    robots,
    subdomain_enum,
    tech_fingerprint,
    crawl_urls,
    web_scrape,
    domain_details,
    social_media_osint
)
from .prompt.agent_prompt import SYSTEM_PROMPT

load_dotenv()

def build_graph():

    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME"),
        base_url=os.getenv("BASE_URL"),
        api_key=os.getenv("GOOGLE_AI_STUDIO_API_KEY"),
        temperature=0.5
    )

    tools = [
        scan_port,
        robots,
        subdomain_enum,
        tech_fingerprint,
        crawl_urls,
        web_scrape,
        domain_details,
        social_media_osint
    ]

    agent = create_react_agent(
        llm,
        tools,
        prompt = SYSTEM_PROMPT
    )

    return agent