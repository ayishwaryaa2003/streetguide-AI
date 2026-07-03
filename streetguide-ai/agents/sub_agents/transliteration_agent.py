from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig

from ..prompts import load_prompt


transliteration_agent = Agent(
    name="transliteration_agent",
    model="gemini-2.5-flash",
    description="Converts multilingual street sign text into Latin script.",
    instruction=load_prompt("transliteration.md"),

    mode="task",
    output_key="transliteration",

    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,

    generate_content_config=GenerateContentConfig(
        temperature=0,
    ),
)