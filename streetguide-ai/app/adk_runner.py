from dotenv import load_dotenv
load_dotenv()

import mimetypes
import uuid
from pathlib import Path

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.genai.errors import ClientError

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

    async def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        await self.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )
        return session_id

    async def _get_partial_state(self, session_id: str) -> dict:
        """Fetch whatever session.state exists, even after a failed run."""
        try:
            session = await self.session_service.get_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_id,
            )
            if session:
                return dict(session.state)
        except Exception as e:
            print(f"⚠️ Could not fetch partial state: {e}")
        return {}

    @staticmethod
    def load_image_part(image_path: str) -> types.Part:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type is None:
            mime_type = "image/jpeg"
        return types.Part.from_bytes(data=path.read_bytes(), mime_type=mime_type)

    @staticmethod
    def print_divider():
        print("\n" + "=" * 70)

    @staticmethod
    def print_agent(author: str):
        print("\n" + "-" * 70)
        print(f"🤖 Agent : {author}")
        print("-" * 70)

    @staticmethod
    def print_text(text: str):
        print(text)

    async def run(self, image_path: str, user_prompt: str):
        session_id = await self.create_session()

        prompt = f"""
User Request:
{user_prompt}

Local Image Path:
{image_path}
""".strip()

        content = types.Content(
            role="user",
            parts=[
                types.Part(text=prompt),
                self.load_image_part(image_path),
            ],
        )

        final_response = ""
        last_author = None

        try:
            self.print_divider()
            print("🚀 StreetGuide AI Workflow Started")
            self.print_divider()

            async for event in self.runner.run_async(
                user_id=USER_ID,
                session_id=session_id,
                new_message=content,
            ):
                
                if event.actions and event.actions.state_delta:
                    print(f"📝 state_delta from {getattr(event, 'author', '?')}: {event.actions.state_delta}")

                author = getattr(event, "author", "Unknown")
                if author != last_author:
                    self.print_agent(author)
                    last_author = author

                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if getattr(part, "text", None):
                            self.print_text(part.text)
                        elif getattr(part, "function_call", None):
                            print("🔧 Function Call:")
                            print(part.function_call)
                        elif getattr(part, "function_response", None):
                            print("✅ Function Response:")
                            print(part.function_response.response)

                if event.is_final_response():
                    if event.content and event.content.parts:
                        part = event.content.parts[0]
                        if getattr(part, "text", None):
                            final_response = part.text
                        elif getattr(part, "function_response", None):
                            final_response = str(part.function_response.response)

            self.print_divider()
            print("✅ Workflow Completed")
            self.print_divider()

            return {
                "success": True,
                "response": final_response,
                "session_id": session_id,
            }

        except ClientError as e:
            is_quota_error = getattr(e, "code", None) == 429

            self.print_divider()
            print("❌ Gemini API error" + (" — QUOTA EXCEEDED" if is_quota_error else ""))
            self.print_divider()
            print(e)

            partial_state = await self._get_partial_state(session_id)
            print(f"📦 Partial session state recovered: {list(partial_state.keys())}")

            return {
                "success": False,
                "error": "Gemini API quota exceeded" if is_quota_error else str(e),
                "quota_exceeded": is_quota_error,
                "session_id": session_id,
                "partial_state": partial_state,  # <-- vision/text outputs likely still here
            }

        except Exception as e:
            self.print_divider()
            print("❌ Workflow Failed")
            self.print_divider()
            print(type(e).__name__)
            print(e)

            import traceback
            traceback.print_exc()

            partial_state = await self._get_partial_state(session_id)

            return {
                "success": False,
                "error": str(e),
                "session_id": session_id,
                "partial_state": partial_state,
            }


adk_runner = ADKRunner()