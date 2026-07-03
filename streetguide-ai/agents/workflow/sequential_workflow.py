from google.adk.agents import SequentialAgent

from ..sub_agents.vision_agent import vision_agent
from ..sub_agents.ocr_agent import ocr_agent
from ..sub_agents.language_agent import language_agent
from ..sub_agents.transliteration_agent import transliteration_agent
from ..sub_agents.navigation_agent import navigation_agent


streetguide_workflow = SequentialAgent(
    name="streetguide_workflow",
    description="StreetGuide AI processing pipeline.",

    sub_agents=[
        vision_agent,
        ocr_agent,
        language_agent,
        transliteration_agent,
        navigation_agent,
    ],
)