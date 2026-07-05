import json
import re
from typing import Dict, Union


def classify_navigation(input_data: Union[str, Dict]):
    """
    Classifies transliterated street sign text into navigation categories.

    Supports two input formats.

    Format 1 (Current):

    {
        "language": "Tamil",
        "transliterated_text": "Chennai\nManagaratchi"
    }

    Format 2 (Future):

    {
        "success": true,
        "items": [
            {
                "line_number": 1,
                "original_text": "சென்னை",
                "transliterated_text": "Chennai"
            }
        ]
    }
    """

    # --------------------------------------------------
    # Convert JSON string to dictionary if needed
    # --------------------------------------------------

    if isinstance(input_data, str):
        input_data = json.loads(input_data)

    # --------------------------------------------------
    # Build a common items list
    # --------------------------------------------------

    if "items" in input_data:

        items = input_data["items"]

    else:

        items = [{
            "line_number": 1,
            "original_text": "",
            "transliterated_text": input_data.get(
                "transliterated_text",
                ""
            )
        }]

    results = []

    # --------------------------------------------------
    # Classification
    # --------------------------------------------------

    for item in items:

        original = item.get("original_text", "")

        transliterated = item.get(
            "transliterated_text",
            ""
        )

        line_no = item.get("line_number", 1)

        text = transliterated.lower()

        category = "Other"
        interpretation = ""

        # Highway

        if "nh" in text or "highway" in text:

            category = "Highway"

            interpretation = "National Highway reference"

        # Distance

        elif re.search(
            r"\b\d+(\.\d+)?\s*(km|m)\b",
            text,
        ):

            category = "Distance"

            interpretation = "Distance indicator"

        # Direction

        elif any(

            word in text

            for word in [

                "left",

                "right",

                "straight",

                "turn",

                "u-turn",

                "north",

                "south",

                "east",

                "west"

            ]

        ):

            category = "Direction"

            interpretation = "Directional instruction"

        # Traffic Rule

        elif any(

            word in text

            for word in [

                "stop",

                "yield",

                "go",

                "no entry",

                "speed limit",

                "one way",

                "give way"

            ]

        ):

            category = "Traffic Rule"

            interpretation = "Traffic regulation"

        # Place Name

        elif transliterated.replace(
            " ",
            ""
        ).isalpha():

            category = "Place Name"

            interpretation = (
                "Geographic location or landmark"
            )

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

        "message": "Navigation analysis completed successfully."

    }