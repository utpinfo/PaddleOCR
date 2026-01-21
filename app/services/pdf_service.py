from pathlib import Path

from PIL import ImageEnhance, Image
from pdf2image import convert_from_path

from app.services.ocr_service import ocr_images, IMAGE_EXTENSIONS
from app.core.config import UPLOAD_DIR, DPI


MAX_SIZE = 2000    # 長邊最大尺寸

def convert_pdf_to_images(
    pdf_path: Path,
    output_dir: Path = None
) -> list[Path]:
    if output_dir is None:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_images"
    output_dir.mkdir(parents=True, exist_ok=True)

    images = convert_from_path(pdf_path, dpi=DPI, thread_count=4)

    img_paths = []
    stem = pdf_path.stem

    for i, pil_img in enumerate(images, 1):
        # 轉灰階 → 增強對比 → 銳化
        img = pil_img.convert("L")
        img = ImageEnhance.Contrast(img).enhance(1.3)
        img = ImageEnhance.Sharpness(img).enhance(1.2)

        # 限制長邊尺寸，避免 PaddleOCR 過慢或記憶體問題
        w, h = img.size
        if max(w, h) > MAX_SIZE:
            ratio = MAX_SIZE / max(w, h)
            new_size = (int(w * ratio), int(h * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        path = output_dir / f"{stem}_page_{i:03d}.png"
        img.save(path, "PNG", optimize=True)
        img_paths.append(path)

    return img_paths


def file_to_text(
        file_path: Path,
        output_dir: Path = UPLOAD_DIR
) -> str:
    ext = file_path.suffix.lower()

    if ext == ".pdf":
        # ✅ 不再判斷文字型 / 圖片型
        img_paths = convert_pdf_to_images(file_path, output_dir)
        return ocr_images(img_paths)

    elif ext in IMAGE_EXTENSIONS:
        return ocr_images([file_path])

    else:
        raise ValueError(f"Unsupported file type: {ext}")
