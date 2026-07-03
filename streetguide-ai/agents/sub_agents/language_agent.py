from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig

from ..prompts import load_prompt


language_agent = Agent(
    name="language_agent",
    model="gemini-2.5-flash",

    description="Identifies the language and writing script of OCR extracted text.",

    instruction=load_prompt("language.md"),

    mode="task",

    output_key="language",

    generate_content_config=GenerateContentConfig(
        temperature=0,
    ),
)