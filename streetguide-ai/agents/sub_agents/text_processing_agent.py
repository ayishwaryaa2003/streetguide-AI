from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig
from ..prompts import load_prompt

text_processing_agent = Agent(
    name="text_processing_agent",
    model="gemini-2.5-flash",
    description="Performs language detection and transliteration in one step.",

    instruction=load_prompt("text_processing.md"),

    mode="task",
    output_key="text_processing",

    generate_content_config=GenerateContentConfig(
        temperature=0,
    ),
)