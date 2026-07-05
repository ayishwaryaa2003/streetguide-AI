from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig

from ..prompts import load_prompt
from ..tools import image_tools


# vision_agent.py
from app.schemas import VisionOutput

# vision_agent.py
from ..core.callbacks import capture_finish_task_output

vision_agent = Agent(
    name="vision_agent",
    model="gemini-2.5-flash",
    description="Analyzes street sign images before OCR.",
    instruction=load_prompt("vision.md"),
    tools=image_tools,
    mode="task",
    output_key="vision",
    after_tool_callback=capture_finish_task_output("vision"),
    generate_content_config=GenerateContentConfig(temperature=0),
)