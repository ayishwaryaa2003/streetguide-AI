import time

from app.adk_runner import adk_runner


async def process_uploaded_image(
    image_path: str,
    source_language: str,
    target_language: str,
):

    start = time.time()

    prompt = f"""
Translate the uploaded street sign.

Source Language:
{source_language}

Target Language:
{target_language}
"""

    response = await adk_runner.run(
        image_path=image_path,
        user_prompt=prompt,
    )

    return {
        "success": True,

        "ocr_text": "",

        "transliterated_text": "",

        "navigation": response,

        "processing_time": round(
            time.time() - start,
            2,
        ),
    }