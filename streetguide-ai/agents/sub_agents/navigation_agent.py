from google.adk.agents import Agent

from agents.prompts import load_prompt
from ..tools.navigation_tools import classify_navigation

# navigation_agent = Agent(
#     name="navigation_agent",
#     description="Classifies street sign text into navigation categories using local rules.",
#     # instruction=load_prompt("navigation.md"),
#     instruction="""
#     You receive the JSON output from Text Processing Agent.

#     Call classify_navigation using that JSON as the input.

#     Return ONLY the tool result.

#     Do not add explanations or markdown.
#     """,
#     tools=[classify_navigation],

#     mode="task",
#     output_key="navigation",

#     disallow_transfer_to_parent=True,
#     disallow_transfer_to_peers=True,
# )

from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig

navigation_agent = Agent(
    name="navigation_agent",

    model="gemini-2.5-flash",

    description="Navigation classifier",

    instruction="""
You MUST call classify_navigation.

Return exactly the tool response.

Do not modify it.
""",

    tools=[classify_navigation],

    mode="task",

    output_key="navigation",

    generate_content_config=GenerateContentConfig(
        temperature=0,
    ),
)