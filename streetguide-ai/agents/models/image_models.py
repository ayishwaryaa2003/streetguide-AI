from dataclasses import dataclass


@dataclass
class ImageValidationResult:
    """
    Result returned after validating an image.
    """

    valid: bool
    message: str


@dataclass
class ImageInfo:
    """
    Metadata about an image.
    """

    filename: str
    format: str
    mode: str
    width: int
    height: int