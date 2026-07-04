# from google.adk.agents.llm_agent import Agent
# from google.genai.types import GenerateContentConfig

# from ..prompts import load_prompt


# ocr_agent = Agent(
#     name="ocr_agent",
#     model="gemini-2.5-flash",

#     description="Extracts visible text from uploaded street sign images.",

#     instruction=load_prompt("ocr.md"),

#     mode="task",

#     output_key="ocr",

#     generate_content_config=GenerateContentConfig(
#         temperature=0,
#     ),
# )