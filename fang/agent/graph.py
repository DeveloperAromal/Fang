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
        prompt = """
            You are an autonomous cybersecurity reconnaissance agent.

When given a target:
1. First enumerate subdomains.
2. Then scan open ports.
3. Then crawl URLs.
4. Then fingerprint technologies.
5. Then collect OSINT data.

Do not ask the user what to do.
Start executing immediately using available tools.
        """
    )

    return agent