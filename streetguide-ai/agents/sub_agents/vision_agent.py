from google.adk.agents.llm_agent import Agent
from ..prompts import load_prompt

from google.adk.tools import FunctionTool

from ..tools import image_tools

vision_agent = Agent(
    name="vision_agent",
    model="gemini-2.5-flash",
    description="Analyzes street sign images before OCR.",
    instruction=load_prompt("vision.md"),
    tools=image_tools,
)