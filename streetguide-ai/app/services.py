import json
import time

from app.adk_runner import adk_runner
from app.parsers import parse_workflow_state

from app.config import USE_MOCK
from app.mocks import get_mock_response

async def process_uploaded_image(
    image_path: str,
    source_language: str,
    target_language: str,
):

    if USE_MOCK:
        return get_mock_response()
    
            # Existing ADK workflow continues here...
    start = time.time()

    prompt = f"""
Translate the uploaded street sign.

Source Language:
{source_language}

Target Language:
{target_language}
"""

    result = await adk_runner.run(

        image_path=image_path,

        user_prompt=prompt,

    )

    if not result["success"]:

        return {

            "success": False,

            "ocr_text": "",

            "transliterated_text": "",

            "navigation": "",

            "error": result["error"],

            "processing_time": round(
                time.time() - start,
                2,
            ),
        }

    session = await adk_runner.session_service.get_session(

        app_name="streetguide_ai",

        user_id="developer",

        session_id=result["session_id"],
    )

    print("\n" + "=" * 80)
    print("SESSION STATE")
    print("=" * 80)

    print(json.dumps(session.state, indent=4))

    print("=" * 80)

    parsed = parse_workflow_state(
        session.state
    )

    return {

        "success": True,

        "processing_time": round(
            time.time() - start,
            2,
        ),

        "image_valid":
            parsed["image_valid"],

        "image_info":
            parsed["image_info"],

        "ocr_text":
            parsed["ocr_text"],

        "language":
            parsed["language"],

        "transliterated_text":
            parsed["transliterated_text"],

        "navigation":
            parsed["navigation"],

        "agent_status": {

            "vision": "completed",

            "text_processing": "completed",

            "navigation": "completed",

        }

    }