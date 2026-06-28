from google.adk.agents.llm_agent import Agent

from ..prompts import load_prompt

transliteration_agent = Agent(
    name="transliteration_agent",
    model="gemini-2.5-flash",
    description="Transliterates text into Latin script.",
    instruction=load_prompt("transliteration.md")
)