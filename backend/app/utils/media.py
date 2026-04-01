from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def build_media_url(image_path: str | None) -> str | None:
    if not image_path:
        return None
    return f"{settings.media_url}/{image_path}"


async def save_upload(upload: UploadFile) -> str:
    if upload.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported image type. Use JPEG, PNG, or WEBP.",
        )

    content = await upload.read()
    max_size_bytes = settings.max_upload_size_mb * 1024 * 1024

    if len(content) > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds {settings.max_upload_size_mb}MB limit.",
        )

    extension = ALLOWED_IMAGE_TYPES[upload.content_type]
    file_name = f"{uuid4().hex}{extension}"
    destination = Path(settings.media_root) / file_name
    destination.write_bytes(content)
    return file_name

