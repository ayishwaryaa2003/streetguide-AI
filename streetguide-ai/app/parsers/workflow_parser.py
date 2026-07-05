"""
Parses the ADK workflow state into a frontend-friendly response.
"""

import json


def _parse_json(value):
    """
    Convert JSON string -> dict if required.
    """

    if value is None:
        return {}

    if isinstance(value, dict):
        return value

    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return {}

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