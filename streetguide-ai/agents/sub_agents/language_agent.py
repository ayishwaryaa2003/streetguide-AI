from google.adk.agents.llm_agent import Agent

from ..prompts import load_prompt

language_agent = Agent(
    name="language_agent",
    model="gemini-2.5-flash",
    description="Detects the language and script.",
    instruction=load_prompt("language.md")
)