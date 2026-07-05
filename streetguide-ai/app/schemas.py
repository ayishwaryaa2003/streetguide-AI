# app/schemas.py
from typing import List, Optional

from pydantic import BaseModel, Field

# agents/models/schemas.py  (new file, or add to existing models folder)

class ImageInfo(BaseModel):
    width: int
    height: int
    format: str

class VisionOutput(BaseModel):
    image_valid: bool
    image_info: ImageInfo | None = None
    ocr_text: str = ""
    reason: str | None = None  # present only when image_valid is False

class TextProcessingOutput(BaseModel):
    language: str
    transliterated_text: str


class NavigationItem(BaseModel):
    line_number: int
    original_text: str
    transliterated_text: str
    category: str
    interpretation: str


class NavigationResponse(BaseModel):
    success: bool = False
    total_items: int = 0
    navigation_items: List[NavigationItem] = Field(default_factory=list)
    message: Optional[str] = None


class ProcessImageResponse(BaseModel):
    success: bool
    ocr_text: str = ""
    transliterated_text: str = ""
    navigation: NavigationResponse = Field(default_factory=NavigationResponse)
    processing_time: float