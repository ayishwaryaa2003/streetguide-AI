# app/services.py
import json
import time

from app.adk_runner import adk_runner
from app.parsers import parse_workflow_state

from app.config import USE_MOCK
from app.mocks import get_mock_response

EMPTY_PARSED = {
    "ocr_text": "",
    "transliterated_text": "",
    "image_valid": False,
    "image_info": {},
    "language": "",
    "navigation": {},
}


async def process_uploaded_image(
    image_path: str,
    source_language: str,
    target_language: str,
):
    if USE_MOCK:
        return get_mock_response()

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
        # Salvage whatever Vision/Text Processing already committed
        # before Navigation hit the quota error.
        partial_state = result.get("partial_state", {})
        parsed = parse_workflow_state(partial_state) if partial_state else EMPTY_PARSED

        print("\n" + "=" * 80)
        print("PARTIAL STATE ON FAILURE")
        print("=" * 80)
        print(json.dumps(partial_state, indent=4))
        print("=" * 80)

        return {
            "success": False,
            "ocr_text": parsed["ocr_text"],
            "transliterated_text": parsed["transliterated_text"],
            "navigation": {
                "success": False,
                "total_items": 0,
                "navigation_items": [],
                "message": result["error"],  # now actually surfaces to the client
            },
            "processing_time": round(time.time() - start, 2),
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

    parsed = parse_workflow_state(session.state)

    navigation = parsed["navigation"]
    if not navigation:
        # Navigation Agent ran but produced no output_key (e.g. died mid-call)
        navigation = {
            "success": False,
            "total_items": 0,
            "navigation_items": [],
            "message": "Navigation data unavailable.",
        }

    return {
        "success": True,
        "processing_time": round(time.time() - start, 2),
        "image_valid": parsed["image_valid"],
        "image_info": parsed["image_info"],
        "ocr_text": parsed["ocr_text"],
        "language": parsed["language"],
        "transliterated_text": parsed["transliterated_text"],
        "navigation": navigation,
        "agent_status": {
            "vision": "completed" if parsed["ocr_text"] else "failed",
            "text_processing": "completed" if parsed["transliterated_text"] else "failed",
            "navigation": "completed" if navigation.get("success") else "failed",
        },
    }