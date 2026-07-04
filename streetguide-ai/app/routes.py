from pathlib import Path
import shutil

from fastapi import APIRouter, File, Form, UploadFile

from app.schemas import ProcessImageResponse
from app.services import process_uploaded_image

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post(
    "/process-image",
    response_model=ProcessImageResponse,
)
async def process_image(
    image: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
):

    image_path = UPLOAD_DIR / image.filename

    with image_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    result = await process_uploaded_image(
        str(image_path),
        source_language,
        target_language,
    )

    return result