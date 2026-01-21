import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File

from app.services.invoice_classifier import classify_invoice, parse_invoice_by_type
from app.services.response_builder import build_response_json
from app.services.pdf_service import file_to_text
from app.core.config import UPLOAD_DIR

router = APIRouter()


@router.get("/ocr/run")
def run_ocr(filename: str):
    """
    對指定上傳資料夾的檔案進行 OCR
    URL: /ocr/run?filename=example.pdf
    或  /ocr/run?filename=example.png
    """
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        return {"error": "File not found"}

    try:
        text = file_to_text(file_path, output_dir=UPLOAD_DIR)

        return {
            "type": "ocr",
            "filename": filename,
            "text": text
        }

    except Exception as e:
        return {"error": str(e)}


@router.post("/ocr/upload_pdf")
async def ocr_upload_file(file: UploadFile = File(...)):
    try:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        # 每個檔案獨立資料夾
        file_subdir = UPLOAD_DIR / Path(file.filename).stem
        file_subdir.mkdir(parents=True, exist_ok=True)

        file_path = file_subdir / file.filename
        with file_path.open("wb") as f:
            shutil.copyfileobj(file.file, f)

        # ✅ 統一入口：OCR
        text = file_to_text(file_path, output_dir=file_subdir)

        # 票據分類
        invoice_info = classify_invoice(text, threshold=50)
        subtype = invoice_info["SubType"]

        invoice_detail = parse_invoice_by_type(text, subtype)

        json_result = build_response_json(text, invoice_info, page=1)
        json_result["Response"]["MixedInvoiceItems"][0]["SingleInvoiceInfos"][subtype] = invoice_detail

        return json_result

    except Exception as e:
        return {"error": str(e)}
