"""
Development runner for StreetGuide AI.
"""
from dotenv import load_dotenv
load_dotenv()

import asyncio
from pathlib import Path
import mimetypes

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from agents import root_agent
from google.genai import types


APP_NAME = "streetguide_ai"
USER_ID = "developer"
SESSION_ID = "dev_session"

def load_image_part(image_path: str) -> types.Part:
    """
    Load an image from disk and convert it into a Gemini Part.
    """

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(path)

    if mime_type is None:
        mime_type = "image/jpeg"

    image_bytes = path.read_bytes()

    return types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type,
    )


async def main():
    # Create an in-memory session service
    session_service = InMemorySessionService()

    # Create a new session
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    # Create the ADK Runner
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("=" * 60)
    print("StreetGuide AI Development Console")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:
        image_path = input("\nImage path (leave blank for text only): ").strip()

        if image_path.lower() == "exit":
            break

        user_input = input("Prompt: ").strip()

        if user_input.lower() == "exit":
            break

        if image_path:
            prompt = f"""
        User Request:
        {user_input}

        Local Image Path:
        {image_path}
        """.strip()
        else:
            prompt = user_input

        parts = [
            types.Part(text=prompt)
        ]

        if image_path:
            try:
                parts.append(load_image_part(image_path))
            except Exception as e:
                print(f"\nError loading image: {e}")
                continue

        print("\nSending request...")

        for i, part in enumerate(parts, start=1):
            if part.text:
                print(f"  Part {i}: TEXT")
            elif part.inline_data:
                print(f"  Part {i}: IMAGE ({part.inline_data.mime_type})")

        content = types.Content(
            role="user",
            parts=parts,
        )

        print("\nAssistant:")

        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    part = event.content.parts[0]

                    if part.text:
                        print(part.text)
                    elif part.function_response:
                        print(part.function_response.response)

if __name__ == "__main__":
    asyncio.run(main())