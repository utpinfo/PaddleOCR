import os
import shutil

from fastapi import APIRouter, UploadFile, File

from app.services.invoice_classifier import classify_invoice, parse_invoice_by_type
from app.services.pdf_service import is_text_pdf, extract_text_from_pdf, pdf_to_images
from app.services.ocr_service import ocr_images
from app.core.config import PDF_PATH
from app.services.response_builder import build_response_json

router = APIRouter()
UPLOAD_DIR = "uploaded_pdfs"

@router.get("/ocr/run")
def run_ocr():
    """對指定 PDF 進行 OCR / 文字抽取"""
    if is_text_pdf(PDF_PATH):
        text = extract_text_from_pdf(PDF_PATH)
        return {"type": "text_pdf", "text": text}
    else:
        img_paths = pdf_to_images(PDF_PATH)
        text = ocr_images(img_paths)
        return {"type": "scanned_pdf", "text": text}


@router.post("/ocr/upload_pdf")
async def ocr_upload_pdf(file: UploadFile = File(...)):
    try:
        # 確保目錄存在
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # 存檔
        pdf_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(pdf_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # 判斷 PDF 類型
        if is_text_pdf(pdf_path):
            text = extract_text_from_pdf(pdf_path)
            pdf_type = "text_pdf"
        else:
            img_paths = pdf_to_images(pdf_path)
            text = ocr_images(img_paths)
            pdf_type = "scanned_pdf"

        # 分類
        invoice_info = classify_invoice(text, threshold=80)

        # 根據票種解析明細
        subtype = invoice_info["SubType"]
        invoice_detail = parse_invoice_by_type(text, subtype)
        # 封裝到 JSON 模板
        json_result = build_response_json(text, invoice_info, page=1)
        json_result["Response"]["MixedInvoiceItems"][0]["SingleInvoiceInfos"][subtype] = invoice_detail

        return json_result

    except Exception as e:
        # 返回錯誤訊息，避免 500
        return {"error": str(e)}
