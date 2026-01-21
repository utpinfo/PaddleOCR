from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
from app.core.config import UPLOAD_DIR, DPI
import os

def is_text_pdf(pdf_path: str) -> bool:
    """判斷是否為文字型 PDF"""
    try:
        text = extract_text(pdf_path)
        return len(text.strip()) > 50
    except Exception:
        return False

def extract_text_from_pdf(pdf_path: str) -> str:
    """文字型 PDF 直接抽文字"""
    return extract_text(pdf_path)

def pdf_to_images(pdf_path: str):
    """掃描 PDF → 轉成 PIL Image 列表"""
    images = convert_from_path(pdf_path, dpi=DPI)
    img_paths = []
    for idx, img in enumerate(images, start=1):
        img_path = os.path.join(UPLOAD_DIR, f"page_{idx}.png")
        img.save(img_path, "PNG")
        img_paths.append(img_path)
    return img_paths
