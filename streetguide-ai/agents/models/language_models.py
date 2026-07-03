from pydantic import BaseModel, Field


class DetectedLanguage(BaseModel):
    """
    Language information for a single OCR line.
    """

    line_number: int = Field(
        description="OCR line number."
    )

    text: str = Field(
        description="Original extracted text."
    )

    language: str = Field(
        description="Detected language."
    )

    language_code: str = Field(
        description="ISO 639-1 language code."
    )

    script: str = Field(
        description="Detected writing script."
    )

    confidence: float = Field(
        description="Confidence score between 0 and 1."
    )


class LanguageResult(BaseModel):
    """
    Output of the Language Agent.
    """

    success: bool

    total_lines: int

    languages: list[DetectedLanguage]

    message: str