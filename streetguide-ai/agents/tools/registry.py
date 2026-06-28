from google.adk.tools import FunctionTool

from .image_utils import (
    validate_image,
    get_image_info,
    resize_image,
    convert_to_rgb,
)

# Image processing tools
image_tools = [
    FunctionTool(validate_image),
    FunctionTool(get_image_info),
]