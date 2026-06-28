from google.adk.agents.llm_agent import Agent

from ..prompts import load_prompt

navigation_agent = Agent(
    name="navigation_agent",
    model="gemini-2.5-flash",
    description="Provides navigation-related information.",
    instruction=load_prompt("navigation.md")
)