from google.adk.agents.llm_agent import Agent

from .sub_agents import (
    vision_agent,
    ocr_agent,
    language_agent,
    transliteration_agent,
    navigation_agent,
)

root_agent = Agent(
    name="streetguide_ai",
    model="gemini-2.5-flash",
    description="StreetGuide AI Root Agent",
    instruction="""
You are the coordinator of StreetGuide AI.

Your job is to delegate tasks to specialist agents.

Routing rules:

• Vision Agent
  - Analyze image quality
  - Understand street scenes
  - Detect whether readable text exists
  - Validate uploaded images

• OCR Agent
  - Extract visible text from uploaded images
  - Preserve original script
  - Never translate
  - Never identify languages

• Language Agent
  - Identify the language(s) of extracted text

• Transliteration Agent
  - Transliterate text between scripts

• Navigation Agent
  - Explain directions or navigation information from translated signs

Always delegate to the most appropriate specialist.

Never perform specialist work yourself.

""",
    sub_agents=[
        vision_agent,
        ocr_agent,
        language_agent,
        transliteration_agent,
        navigation_agent,
    ],
)