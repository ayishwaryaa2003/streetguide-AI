from pydantic import BaseModel, Field


class NavigationItem(BaseModel):
    """
    Represents one navigation-related item extracted from the text.
    """

    line_number: int = Field(
        description="Line number from the OCR output."
    )

    original_text: str = Field(
        description="Original text."
    )

    category: str = Field(
        description=(
            "Navigation category such as Place Name, Direction, "
            "Distance, Highway, Landmark, Traffic Rule or Other."
        )
    )

    interpretation: str = Field(
        description="Human-readable interpretation."
    )


class NavigationResult(BaseModel):
    """
    Output produced by the Navigation Agent.
    """

    success: bool

    total_items: int

    navigation_items: list[NavigationItem]

    message: str