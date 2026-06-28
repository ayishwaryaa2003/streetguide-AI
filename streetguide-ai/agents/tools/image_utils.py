from pathlib import Path
from PIL import Image

from ..models.image_models import (
    ImageValidationResult,
    ImageInfo,
)

SUPPORTED_FORMATS = {"JPEG", "JPG", "PNG", "WEBP"}


def validate_image(image_path: str) -> ImageValidationResult:
    """
    Validate an image before processing.
    """

    path = Path(image_path)

    if not path.exists():
        return ImageValidationResult(
            valid=False,
            message="Image file does not exist."
        )

    try:
        with Image.open(path) as img:

            if img.format.upper() not in SUPPORTED_FORMATS:
                return ImageValidationResult(
                    valid=False,
                    message=f"Unsupported format: {img.format}"
                )

            return ImageValidationResult(
                valid=True,
                message="Image is valid."
            )

    except Exception as e:
        return ImageValidationResult(
            valid=False,
            message=str(e)
        )
    


def get_image_info(image_path: str) -> ImageInfo:
    """
    Return image metadata.
    """

    with Image.open(image_path) as img:
        return ImageInfo(
            filename=Path(image_path).name,
            format=img.format,
            mode=img.mode,
            width=img.width,
            height=img.height,
        )   


def resize_image(
    image_path: str,
    width: int,
    height: int
) -> Image.Image:
    """
    Resize an image.
    """

    img = Image.open(image_path)

    return img.resize((width, height))


def convert_to_rgb(image_path: str) -> Image.Image:
    """
    Convert image to RGB mode.
    """

    img = Image.open(image_path)

    return img.convert("RGB")