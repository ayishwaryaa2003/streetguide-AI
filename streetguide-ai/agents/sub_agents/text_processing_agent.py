from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig
from ..prompts import load_prompt

# text_processing_agent.py
from app.schemas import TextProcessingOutput
from ..core.callbacks import capture_finish_task_output

# text_processing_agent.py
text_processing_agent = Agent(
    name="text_processing_agent",
    model="gemini-2.5-flash",
    description="Performs language detection and transliteration in one step.",
    instruction=load_prompt("text_processing.md"),
    mode="task",
    output_key="text_processing",
    after_tool_callback=capture_finish_task_output("text_processing"),
    generate_content_config=GenerateContentConfig(temperature=0),
)