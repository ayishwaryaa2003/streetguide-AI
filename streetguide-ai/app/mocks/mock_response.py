import random


def get_mock_response():

    processing_time = round(
        random.uniform(1.2, 2.8),
        2,
    )

    return {

        "success": True,

        "processing_time": processing_time,

        "image_valid": True,

        "image_info": {

            "width": 686,

            "height": 386,

            "format": "JPEG"

        },

        "ocr_text":
            "Road signs ஐ\n"
            "ஈஸியா கத்துக்கலாம்",

        "language":
            "Tamil",

        "transliterated_text":
            "Road signs ai\n"
            "Eesiyaa Kaththukkalaam",

        "navigation": {

            "success": True,

            "total_items": 2,

            "navigation_items": [

                {

                    "line_number": 1,

                    "original_text": "Road signs ஐ",

                    "transliterated_text":
                        "Road signs ai",

                    "category": "Place Name",

                    "interpretation":
                        "Geographic location"

                },

                {

                    "line_number": 2,

                    "original_text":
                        "ஈஸியா கத்துக்கலாம்",

                    "transliterated_text":
                        "Eesiyaa Kaththukkalaam",

                    "category": "Other",

                    "interpretation":
                        "General informational text"

                }

            ]

        },

        "agent_status": {

            "vision": "completed",

            "text_processing": "completed",

            "navigation": "completed"

        }

    }