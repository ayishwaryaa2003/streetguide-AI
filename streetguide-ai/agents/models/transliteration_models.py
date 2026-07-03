from pydantic import BaseModel, Field


class TransliteratedLine(BaseModel):
    """
    Transliteration for one OCR line.
    """

    line_number: int = Field(
        description="OCR line number."
    )

    original_text: str = Field(
        description="Original text."
    )

    transliterated_text: str = Field(
        description="Latin-script transliteration."
    )

    language: str = Field(
        description="Detected language."
    )


class TransliterationResult(BaseModel):
    """
    Output of the Transliteration Agent.
    """

    success: bool

    total_lines: int

    transliterations: list[TransliteratedLine]

    message: str