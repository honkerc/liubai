"""文件上传：图片压缩 + 多类型文件安全校验"""

from __future__ import annotations

import os
import re
import uuid
from io import BytesIO
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, UploadFile
from PIL import Image, ImageOps

from config import UPLOAD_DIR_MAX_BYTES, UPLOAD_MAX_FILE_BYTES, UPLOAD_ROOT
IMAGE_ORIGINAL_DIR = UPLOAD_ROOT / "images" / "original"
IMAGE_COMPRESSED_DIR = UPLOAD_ROOT / "images" / "compressed"
VIDEO_DIR = UPLOAD_ROOT / "videos"
AUDIO_DIR = UPLOAD_ROOT / "audio"
FILE_DIR = UPLOAD_ROOT / "files"

COMPRESS_MAX_WIDTH = 1920
COMPRESS_QUALITY = 82

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".ico"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".avi", ".mkv", ".m4v", ".ogv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac"}
ARCHIVE_EXTENSIONS = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"}
FILE_EXTENSIONS = {
    ".pdf", ".md", ".txt",
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
} | ARCHIVE_EXTENSIONS
ALLOWED_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | AUDIO_EXTENSIONS | FILE_EXTENSIONS

BLOCKED_EXTENSIONS = {
    ".svg", ".html", ".htm", ".js", ".jsx", ".ts", ".tsx",
    ".php", ".asp", ".aspx", ".jsp", ".exe", ".bat", ".cmd",
    ".sh", ".bash", ".ps1", ".dll", ".msi", ".jar", ".war",
}

FILENAME_UNSAFE = re.compile(r"[^\w.\- ()\u4e00-\u9fff]", re.UNICODE)


def ensure_upload_dirs() -> None:
    for directory in (
        IMAGE_ORIGINAL_DIR,
        IMAGE_COMPRESSED_DIR,
        VIDEO_DIR,
        AUDIO_DIR,
        FILE_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)


def _safe_display_name(filename: Optional[str]) -> str:
    raw = (filename or "file").strip()
    raw = raw.replace("\x00", "")
    raw = os.path.basename(raw)
    raw = FILENAME_UNSAFE.sub("_", raw)
    return raw[:200] or "file"


def _normalize_ext(filename: Optional[str]) -> str:
    ext = Path(filename or "").suffix.lower()
    if not ext:
        raise HTTPException(status_code=400, detail="无法识别文件类型")
    if ext in BLOCKED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="不允许上传该文件类型")
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    return ext


async def _read_upload(file: UploadFile) -> bytes:
    chunks = []
    total = 0
    while True:
        chunk = await file.read(1024 * 1024)
        if not chunk:
            break
        total += len(chunk)
        if total > UPLOAD_MAX_FILE_BYTES:
            limit_mb = UPLOAD_MAX_FILE_BYTES // (1024 * 1024)
            raise HTTPException(
                status_code=413,
                detail=f"文件过大，单文件上限 {limit_mb} MB",
            )
        chunks.append(chunk)
    return b"".join(chunks)


def _detect_image_ext(data: bytes) -> Optional[str]:
    try:
        with Image.open(BytesIO(data)) as img:
            fmt = (img.format or "").upper()
    except Exception:
        return None
    mapping = {
        "JPEG": ".jpg",
        "PNG": ".png",
        "GIF": ".gif",
        "WEBP": ".webp",
        "BMP": ".bmp",
        "ICO": ".ico",
    }
    return mapping.get(fmt)


def _validate_image_bytes(data: bytes, ext: str) -> None:
    detected = _detect_image_ext(data)
    if detected is None:
        raise HTTPException(status_code=400, detail="无法识别的图片文件")

    normalized = ".jpg" if ext in {".jpg", ".jpeg"} else ext
    detected_norm = ".jpg" if detected == ".jpg" else detected
    if normalized != detected_norm:
        raise HTTPException(status_code=400, detail="文件扩展名与内容不匹配")

    try:
        with Image.open(BytesIO(data)) as img:
            img.verify()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="图片文件无效或已损坏") from exc


def _validate_pdf_bytes(data: bytes) -> None:
    if not data.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="PDF 文件无效")


def _validate_plain_text_bytes(data: bytes) -> None:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="文本文件必须是 UTF-8 编码") from exc


def _validate_zip_bytes(data: bytes) -> None:
    if not (
        data.startswith(b"PK\x03\x04")
        or data.startswith(b"PK\x05\x06")
        or data.startswith(b"PK\x07\x08")
    ):
        raise HTTPException(status_code=400, detail="ZIP 文件无效")


def _validate_rar_bytes(data: bytes) -> None:
    if not (data.startswith(b"Rar!\x1a\x07") or data.startswith(b"Rar!\x1a\x07\x01\x00")):
        raise HTTPException(status_code=400, detail="RAR 文件无效")


def _validate_7z_bytes(data: bytes) -> None:
    if not data.startswith(b"7z\xbc\xaf\x27\x1c"):
        raise HTTPException(status_code=400, detail="7Z 文件无效")


def _validate_gzip_bytes(data: bytes) -> None:
    if not data.startswith(b"\x1f\x8b"):
        raise HTTPException(status_code=400, detail="GZ 文件无效")


def _validate_bzip2_bytes(data: bytes) -> None:
    if not data.startswith(b"BZh"):
        raise HTTPException(status_code=400, detail="BZ2 文件无效")


def _validate_video_bytes(data: bytes, ext: str) -> None:
    if len(data) < 12:
        raise HTTPException(status_code=400, detail="视频文件无效")

    head = data[:32]
    if ext in {".mp4", ".m4v", ".mov"}:
        if b"ftyp" not in head:
            raise HTTPException(status_code=400, detail="视频文件无效")
        return
    if ext == ".webm":
        if not data.startswith(b"\x1a\x45\xdf\xa3"):
            raise HTTPException(status_code=400, detail="视频文件无效")
        return
    if ext == ".avi":
        if not data.startswith(b"RIFF") or b"AVI" not in head:
            raise HTTPException(status_code=400, detail="视频文件无效")
        return
    if ext == ".mkv":
        if not data.startswith(b"\x1a\x45\xdf\xa3"):
            raise HTTPException(status_code=400, detail="视频文件无效")
        return
    if ext == ".ogv":
        if not data.startswith(b"OggS"):
            raise HTTPException(status_code=400, detail="视频文件无效")
        return


def _validate_audio_bytes(data: bytes, ext: str) -> None:
    if len(data) < 4:
        raise HTTPException(status_code=400, detail="音频文件无效")

    if ext == ".mp3":
        if not (data.startswith(b"ID3") or data[:2] in {b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"}):
            raise HTTPException(status_code=400, detail="音频文件无效")
        return
    if ext == ".wav":
        if not (data.startswith(b"RIFF") and b"WAVE" in data[:16]):
            raise HTTPException(status_code=400, detail="音频文件无效")
        return
    if ext == ".ogg":
        if not data.startswith(b"OggS"):
            raise HTTPException(status_code=400, detail="音频文件无效")
        return
    if ext == ".flac":
        if not data.startswith(b"fLaC"):
            raise HTTPException(status_code=400, detail="音频文件无效")
        return
    if ext == ".m4a":
        if b"ftyp" not in data[:32]:
            raise HTTPException(status_code=400, detail="音频文件无效")
        return


def _validate_file_bytes(data: bytes, ext: str) -> None:
    if ext in IMAGE_EXTENSIONS:
        _validate_image_bytes(data, ext)
        return
    if ext in VIDEO_EXTENSIONS:
        _validate_video_bytes(data, ext)
        return
    if ext in AUDIO_EXTENSIONS:
        _validate_audio_bytes(data, ext)
        return
    if ext == ".pdf":
        _validate_pdf_bytes(data)
        return
    if ext in {".md", ".txt"}:
        _validate_plain_text_bytes(data)
        return
    if ext == ".zip":
        _validate_zip_bytes(data)
        return
    if ext == ".rar":
        _validate_rar_bytes(data)
        return
    if ext == ".7z":
        _validate_7z_bytes(data)
        return
    if ext == ".gz":
        _validate_gzip_bytes(data)
        return
    if ext == ".bz2":
        _validate_bzip2_bytes(data)
        return


def _save_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def _compress_image(original_path: Path, compressed_path: Path, ext: str) -> None:
    with Image.open(original_path) as img:
        img = ImageOps.exif_transpose(img)

        if ext == ".gif":
            if img.width > COMPRESS_MAX_WIDTH:
                ratio = COMPRESS_MAX_WIDTH / img.width
                new_size = (COMPRESS_MAX_WIDTH, max(1, int(img.height * ratio)))
                img = img.copy()
                img.thumbnail(new_size, Image.Resampling.LANCZOS)
            img.save(compressed_path, format="GIF", optimize=True)
            return

        if ext == ".ico":
            img.save(compressed_path, format="ICO")
            return

        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            converted = img.convert("RGBA")
            if converted.width > COMPRESS_MAX_WIDTH:
                ratio = COMPRESS_MAX_WIDTH / converted.width
                new_size = (COMPRESS_MAX_WIDTH, max(1, int(converted.height * ratio)))
                converted = converted.copy()
                converted.thumbnail(new_size, Image.Resampling.LANCZOS)
            converted.save(compressed_path, format="WEBP", quality=COMPRESS_QUALITY, method=6)
            return

        converted = img.convert("RGB")
        if converted.width > COMPRESS_MAX_WIDTH:
            ratio = COMPRESS_MAX_WIDTH / converted.width
            new_size = (COMPRESS_MAX_WIDTH, max(1, int(converted.height * ratio)))
            converted = converted.copy()
            converted.thumbnail(new_size, Image.Resampling.LANCZOS)
        converted.save(compressed_path, format="WEBP", quality=COMPRESS_QUALITY, method=6)


def _public_url(path: Path) -> str:
    rel = path.relative_to(UPLOAD_ROOT).as_posix()
    return f"/uploads/{rel}"


def _compressed_name(stem: str, original_ext: str) -> str:
    if original_ext == ".gif":
        return f"{stem}.gif"
    if original_ext == ".ico":
        return f"{stem}.ico"
    return f"{stem}.webp"


def _media_type(ext: str) -> str:
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    if ext in AUDIO_EXTENSIONS:
        return "audio"
    return "file"


async def save_upload(file: UploadFile) -> dict:
    ensure_upload_dirs()

    display_name = _safe_display_name(file.filename)
    ext = _normalize_ext(file.filename)
    media_type = _media_type(ext)

    data = await _read_upload(file)
    if not data:
        raise HTTPException(status_code=400, detail="文件为空")

    _validate_file_bytes(data, ext)

    stem = uuid.uuid4().hex

    if media_type == "image":
        original_name = f"{stem}{ext}"
        original_path = IMAGE_ORIGINAL_DIR / original_name
        _save_bytes(original_path, data)

        compressed_name = _compressed_name(stem, ext)
        compressed_path = IMAGE_COMPRESSED_DIR / compressed_name
        try:
            _compress_image(original_path, compressed_path, ext)
        except Exception as exc:
            original_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail="图片处理失败") from exc

        original_url = _public_url(original_path)
        compressed_url = _public_url(compressed_path)

        return {
            "type": "image",
            "filename": display_name,
            "url": compressed_url,
            "original_url": original_url,
            "compressed_url": compressed_url,
            "size": len(data),
        }

    if media_type == "video":
        dest = VIDEO_DIR / f"{stem}{ext}"
    elif media_type == "audio":
        dest = AUDIO_DIR / f"{stem}{ext}"
    else:
        dest = FILE_DIR / f"{stem}{ext}"

    _save_bytes(dest, data)
    file_url = _public_url(dest)

    return {
        "type": media_type,
        "filename": display_name,
        "url": file_url,
        "original_url": file_url,
        "compressed_url": None,
        "size": len(data),
    }


def _upload_dir_size() -> int:
    total = 0
    if not UPLOAD_ROOT.exists():
        return 0
    for path in UPLOAD_ROOT.rglob("*"):
        if path.is_file():
            try:
                total += path.stat().st_size
            except OSError:
                continue
    return total


def cleanup_uploads_if_needed(max_bytes: int | None = None) -> int:
    """超出容量上限时按修改时间删除最旧文件，返回删除数量"""
    limit = max_bytes if max_bytes is not None else UPLOAD_DIR_MAX_BYTES
    removed = 0

    while _upload_dir_size() > limit:
        files = [
            path for path in UPLOAD_ROOT.rglob("*")
            if path.is_file()
        ]
        if not files:
            break

        oldest = min(files, key=lambda p: p.stat().st_mtime)
        try:
            oldest.unlink(missing_ok=True)
            removed += 1
        except OSError:
            break

    return removed
