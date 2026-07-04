def default_pipeline_state():
    return {
        "image_valid": False,
        "vision": {},
        "ocr": {
            "success": False,
            "lines": []
        },
        "language": {
            "success": False,
            "languages": []
        },
        "transliteration": {
            "success": False,
            "transliterations": []
        },
        "navigation": {
            "success": False,
            "navigation_items": []
        }
    }