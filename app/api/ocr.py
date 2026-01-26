import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File
from llama_cpp import Llama
from transformers import AutoTokenizer

from app.services.invoice_classifier import classify_invoice, parse_invoice_by_type
from app.services.response_builder import build_response_json
from app.services.pdf_service import file_to_text
from app.core.config import UPLOAD_DIR
from fastapi import Request

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


# 初始化一次
model_path = "/opt/Models"
gguf_path = f"{model_path}/Qwen_Qwen3-30B-A3B-Q5_K_M.gguf"
tokenizer = AutoTokenizer.from_pretrained(f"{model_path}/Qwen3-30B-A3B", local_files_only=True, trust_remote_code=True)
model = Llama(model_path=gguf_path, n_ctx=4096, n_threads=8,  n_gpu_layers=0)


@router.post("/qwen3/generate")
async def generate(request: Request):
    data = await request.json()  # async
    messages = data.get("messages", [])
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    completion = model(prompt=text, max_tokens=128, echo=False)
    return {"text": completion["choices"][0]["text"]}