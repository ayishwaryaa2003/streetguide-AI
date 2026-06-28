from pydantic import BaseModel, Field


class OCRLine(BaseModel):
    """
    Represents a single line extracted from an image.
    """

    line_number: int = Field(
        description="Line number in reading order."
    )

    text: str = Field(
        description="Exact text extracted from the image."
    )


class OCRResult(BaseModel):
    """
    Structured OCR output.
    """

    success: bool = Field(
        description="Whether OCR completed successfully."
    )

    total_lines: int = Field(
        description="Total number of extracted text lines."
    )

    lines: list[OCRLine] = Field(
        default_factory=list,
        description="List of OCR lines."
    )

    message: str = Field(
        description="Status message."
    )