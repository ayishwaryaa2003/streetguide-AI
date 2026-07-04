from pydantic import BaseModel


class ProcessImageResponse(BaseModel):
    success: bool
    ocr_text: str
    transliterated_text: str
    navigation: str
    processing_time: float