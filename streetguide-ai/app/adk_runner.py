"""
Reusable ADK Runner for StreetGuide AI.

This module is shared by:
1. FastAPI backend
2. Development console
"""
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
import mimetypes
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents import root_agent


APP_NAME = "streetguide_ai"
USER_ID = "developer"


class ADKRunner:

    def __init__(self):

        self.session_service = InMemorySessionService()

        self.runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=self.session_service,
        )

    async def load_session(self):

        session_id = str(uuid.uuid4())

        await self.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )

        return session_id

    @staticmethod
    def load_image_part(image_path: str) -> types.Part:

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(image_path)

        mime_type, _ = mimetypes.guess_type(path)

        if mime_type is None:
            mime_type = "image/jpeg"

        return types.Part.from_bytes(
            data=path.read_bytes(),
            mime_type=mime_type,
        )

    async def run(
        self,
        image_path: str,
        user_prompt: str,
    ) -> str:

        session_id = await self.load_session()

        prompt = f"""
User Request:
{user_prompt}

Local Image Path:
{image_path}
""".strip()

        parts = [
            types.Part(text=prompt),
            self.load_image_part(image_path),
        ]

        content = types.Content(
            role="user",
            parts=parts,
        )

        final_response = ""

        async for event in self.runner.run_async(
            user_id=USER_ID,
            session_id=session_id,
            new_message=content,
        ):

            if event.is_final_response():

                if event.content and event.content.parts:

                    part = event.content.parts[0]

                    if part.text:
                        final_response = part.text

                    elif part.function_response:
                        final_response = str(
                            part.function_response.response
                        )

        return final_response


adk_runner = ADKRunner()