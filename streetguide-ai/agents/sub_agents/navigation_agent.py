from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig

from ..prompts import load_prompt


navigation_agent = Agent(
    name="navigation_agent",
    model="gemini-2.5-flash",

    description="Interprets navigation-related information from street sign text.",

    instruction=load_prompt("navigation.md"),

    mode="task",

    output_key="navigation",

    generate_content_config=GenerateContentConfig(
        temperature=0,
    ),
)