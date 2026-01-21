import os
import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File

from app.services.invoice_classifier import classify_invoice, parse_invoice_by_type
from app.services.pdf_service import is_text_pdf, extract_text_from_pdf, file_to_text
from app.services.ocr_service import ocr_images
from app.core.config import UPLOAD_DIR
from app.services.response_builder import build_response_json

router = APIRouter()


@router.get("/ocr/run")
def run_ocr(filename: str):
    """
    對指定上傳資料夾的檔案進行 OCR / 文字抽取
    URL: /ocr/run?filename=example.pdf
    或  /ocr/run?filename=example.png
    """
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        return {"error": "File not found"}

    try:
        # 使用通用入口
        text = file_to_text(file_path, output_dir=UPLOAD_DIR)

        # 判斷檔案類型
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            file_type = "text_pdf" if is_text_pdf(file_path) else "scanned_pdf"
        else:
            file_type = "image_file"

        return {"type": file_type, "text": text}

    except Exception as e:
        return {"error": str(e)}

@router.post("/ocr/upload_pdf")
async def ocr_upload_file(file: UploadFile = File(...)):
    try:
        # 確保上傳資料夾存在
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        # 每個上傳檔案建立子資料夾，避免同名覆蓋
        file_subdir = UPLOAD_DIR / Path(file.filename).stem
        file_subdir.mkdir(parents=True, exist_ok=True)

        # 存檔
        file_path = file_subdir / file.filename
        with file_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)

        # 通用 OCR / 文字抽取
        from app.api.ocr import file_to_text  # 確保導入
        text = file_to_text(file_path, output_dir=file_subdir)

        # 判斷檔案類型
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            pdf_type = "text_pdf" if is_text_pdf(file_path) else "scanned_pdf"
        else:
            pdf_type = "image_file"

        # 分類票據
        invoice_info = classify_invoice(text, threshold=50)
        subtype = invoice_info["SubType"]
        invoice_detail = parse_invoice_by_type(text, subtype)

        # 封裝 JSON
        json_result = build_response_json(text, invoice_info, page=1)
        json_result["Response"]["MixedInvoiceItems"][0]["SingleInvoiceInfos"][subtype] = invoice_detail

        return json_result

    except Exception as e:
        return {"error": str(e)}
