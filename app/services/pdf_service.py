from pathlib import Path
from PIL import Image
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path

from app.services.ocr_service import ocr_images, IMAGE_EXTENSIONS  # ✅ 導入服務層
from app.core.config import UPLOAD_DIR, DPI

def is_text_pdf(pdf_path: Path) -> bool:
    try:
        text = extract_text(str(pdf_path))
        return len(text.strip()) > 50
    except Exception:
        return False

def extract_text_from_pdf(pdf_path: Path) -> str:
    return extract_text(str(pdf_path))

def convert_pdf_to_images(pdf_path: Path, output_dir: Path = UPLOAD_DIR) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    images = convert_from_path(str(pdf_path), dpi=DPI)
    img_paths: list[Path] = []
    for idx, img in enumerate(images, start=1):
        img_path = output_dir / f"page_{idx}.png"
        img.save(img_path, "PNG")
        img_paths.append(img_path)
    return img_paths

def file_to_text(file_path: Path, output_dir: Path = UPLOAD_DIR) -> str:
    ext = file_path.suffix.lower()
    if ext == ".pdf":
        if is_text_pdf(file_path):
            return extract_text_from_pdf(file_path)
        else:
            img_paths = convert_pdf_to_images(file_path, output_dir)
            return ocr_images(img_paths)
    elif ext in IMAGE_EXTENSIONS:
        return ocr_images([file_path])
    else:
        raise ValueError(f"Unsupported file type: {ext}")
