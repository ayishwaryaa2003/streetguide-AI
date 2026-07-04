from typing import Dict

def transliterate_text(input_data: Dict):
    """
    Local transliteration tool (no Gemini API calls).
    Works on OCR + Language Agent output.
    """

    lines = input_data.get("lines", [])

    results = []

    for line in lines:
        text = line.get("text", "")
        lang = line.get("language", "unknown")

        # TEMP SIMPLE LOGIC (safe for capstone)
        # You can upgrade later using indic-transliteration library
        transliterated = text

        results.append({
            "line_number": line.get("line_number", 0),
            "original_text": text,
            "transliterated_text": transliterated,
            "language": lang
        })

    return {
        "success": True,
        "total_lines": len(results),
        "transliterations": results,
        "message": "Transliteration completed locally (no LLM used)."
    }