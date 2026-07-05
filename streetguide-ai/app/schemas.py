from typing import List

from pydantic import BaseModel


class NavigationItem(BaseModel):
    line_number: int
    original_text: str
    transliterated_text: str
    category: str
    interpretation: str


class NavigationResponse(BaseModel):
    success: bool
    total_items: int
    navigation_items: List[NavigationItem]


class ProcessImageResponse(BaseModel):
    success: bool

    ocr_text: str

    transliterated_text: str

    navigation: NavigationResponse

    processing_time: float