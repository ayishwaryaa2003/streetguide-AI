"""
Parses the ADK workflow state into a frontend-friendly response.
"""

import json


# app/parsers/workflow_parser.py
def _parse_json(value):
    if value is None:
        return {}

    if isinstance(value, str):
        try:
            value = json.loads(value)
        except Exception as e:
            print(f"⚠️ JSON parse failed: {value[:200]!r} — {e}")
            return {}

    if isinstance(value, dict):
        if set(value.keys()) == {"result"} and isinstance(value["result"], str):
            try:
                return json.loads(value["result"])
            except Exception:
                return {}
        return value

    return {}


def parse_workflow_state(state: dict):

    vision = _parse_json(
        state.get("vision")
    )

    text = _parse_json(
        state.get("text_processing")
    )

    navigation = _parse_json(
        state.get("navigation")
    )

    return {

        "ocr_text":
            vision.get(
                "ocr_text",
                ""
            ),

        "image_valid":
            vision.get(
                "image_valid",
                False
            ),

        "image_info":
            vision.get(
                "image_info",
                {}
            ),

        "language":
            text.get(
                "language",
                ""
            ),

        "transliterated_text":
            text.get(
                "transliterated_text",
                ""
            ),

        "navigation":
            navigation,
    }