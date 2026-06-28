from google.adk.agents.llm_agent import Agent

from ..prompts import load_prompt


ocr_agent = Agent(
    name="ocr_agent",
    model="gemini-2.5-flash",
    description="Extracts visible text from uploaded street sign images.",
    instruction=load_prompt("ocr.md"),
)