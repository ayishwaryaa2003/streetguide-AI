from typing import Dict
import re


def classify_navigation(input_data: Dict):
    """
    Receives the JSON output from Text Processing Agent.

    Expected input:

    {
        "success": true,
        "items": [
            {
                "line_number": 1,
                "original_text": "சென்னை",
                "language": "Tamil",
                "language_code": "ta",
                "script": "Tamil",
                "transliterated_text": "Chennai"
            }
        ]
    }
    """

    items = input_data.get("items", [])

    results = []

    for item in items:

        original = item.get("original_text", "")
        transliterated = item.get("transliterated_text", "")
        line_no = item.get("line_number", 0)

        # Use transliterated text for classification
        text = transliterated.lower()

        category = "Other"
        interpretation = ""

        # ---------------------------
        # HIGHWAY
        # ---------------------------
        if "nh" in text or "highway" in text:
            category = "Highway"
            interpretation = "National Highway reference"

        # ---------------------------
        # DISTANCE
        # Detect:
        # 5 km
        # 500 m
        # 12.5 km
        # ---------------------------
        elif re.search(r"\b\d+(\.\d+)?\s*(km|m)\b", text):
            category = "Distance"
            interpretation = "Distance indicator"

        # ---------------------------
        # DIRECTION
        # ---------------------------
        elif any(word in text for word in [
            "left",
            "right",
            "straight",
            "turn",
            "u-turn"
        ]):
            category = "Direction"
            interpretation = "Directional instruction"

        # ---------------------------
        # TRAFFIC RULE
        # ---------------------------
        elif any(word in text for word in [
            "stop",
            "go",
            "yield",
            "no entry",
            "speed limit"
        ]):
            category = "Traffic Rule"
            interpretation = "Traffic regulation"

        # ---------------------------
        # PLACE NAME
        # ---------------------------
        elif transliterated.replace(" ", "").isalpha():
            category = "Place Name"
            interpretation = "Geographic location or landmark"

        results.append({

            "line_number": line_no,

            "original_text": original,

            "transliterated_text": transliterated,

            "category": category,

            "interpretation": interpretation
        })

    return {

        "success": True,

        "total_items": len(results),

        "navigation_items": results,

        "message": "Navigation analysis completed locally (no LLM used)."
    }