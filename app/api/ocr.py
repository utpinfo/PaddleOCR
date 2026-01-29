import os
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File
from llama_cpp import Llama
from transformers import AutoTokenizer

from app.services.invoice_classifier import classify_invoice, parse_invoice_by_type
from app.services.response_builder import build_response_json
from app.services.pdf_service import file_to_text
from app.core.config import UPLOAD_DIR, QWEN_GGUF, QWEN_TOKENIZER, LLAMA_GGUF
from fastapi import Request

# -1：盡量把所有層 offload 到 GPU（llama.cpp 會自動計算能放多少層，不會 OOM）
# 0：完全不 offload，全跑在 CPU（最慢）
n_gpu_layers = 0
n_threads = min(16, os.cpu_count())  # 不要超過 CPU 核心數
n_ctx = 1024  # context 越大越慢

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
tokenizer = AutoTokenizer.from_pretrained(str(QWEN_TOKENIZER), local_files_only=True, trust_remote_code=True)
model = Llama(model_path=str(QWEN_GGUF), n_ctx=n_ctx, n_threads=n_threads, n_gpu_layers=n_gpu_layers)


@router.post("/qwen3/generate")
async def generate(request: Request):
    data = await request.json()  # async
    messages = data.get("messages", [])
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    completion = model(prompt=text, max_tokens=300, echo=False, stop=["<think>", "</think>"])
    return {"text": completion["choices"][0]["text"]}


model = Llama(model_path=str(LLAMA_GGUF), n_ctx=n_ctx, n_threads=n_threads, n_gpu_layers=n_gpu_layers, flash_attn=True)


@router.post("/llama3/generate")
async def generate(request: Request):
    data = await request.json()
    messages = data.get("messages", [])

    prompt = ""
    for m in messages:
        prompt += f"<|start_header_id|>{m['role']}<|end_header_id|>\n\n{m['content']}<|eot_id|>\n\n"
    prompt += "<|start_header_id|>assistant<|end_header_id|>\n\n"

    completion = model(
        prompt,
        max_tokens=512,
        echo=False,
        stop=["<|eot_id|>"],
    )
    return {"text": completion["choices"][0]["text"].strip()}
