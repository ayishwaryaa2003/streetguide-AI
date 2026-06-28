from dataclasses import dataclass
from typing import Optional

from ..models.image_models import (
    ImageInfo,
    ImageValidationResult,
)


@dataclass
class WorkflowState:
    """
    Shared state across all StreetGuide AI agents.
    """

    # Input
    image_path: Optional[str] = None

    # Vision
    image_validation: Optional[ImageValidationResult] = None
    image_info: Optional[ImageInfo] = None

    # OCR
    extracted_text: Optional[str] = None

    # Language
    detected_language: Optional[str] = None
    detected_script: Optional[str] = None

    # Transliteration
    transliterated_text: Optional[str] = None

    # Navigation
    navigation_hint: Optional[str] = None

    # Final Output
    final_response: Optional[str] = None