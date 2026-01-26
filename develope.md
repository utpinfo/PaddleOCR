# PaddleOCR — 中文/高精度場景最強

## Python 安裝套件

```shell
cd PaddleOCR
pyenv install 3.12.11
pip install -r requirements.txt
```

## Mac 額外安裝

```shell
brew install poppler
```

## Debian 額外安裝

```shell
apt update && apt install -y \
    libsm6 libxext6 libxrender-dev libglib2.0-0 ffmpeg poppler-utils
```

# PyCharm配置 (congiguration)

```config
module <- gunicorn
scripts <- -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8001
module <- unicorn
scripts <- app.main:app --host 0.0.0.0 --port 8001 --reload
```

# 範例代碼

```python
import os
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
from paddleocr import PaddleOCR

PDF_PATH = "/Users/yangfengkai/Downloads/AT260100004964022.pdf"
DPI = 300
TEMP_DIR = "pdf_images"


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


def ocr_pdf(pdf_path: str) -> str:
    """掃描 PDF → 圖片 → PaddleOCR"""
    os.makedirs(TEMP_DIR, exist_ok=True)

    ocr = PaddleOCR(
        lang="ch",
        use_angle_cls=True,
        show_log=False
    )

    images = convert_from_path(pdf_path, dpi=DPI)
    all_text = []

    for idx, img in enumerate(images, start=1):
        img_path = os.path.join(TEMP_DIR, f"page_{idx}.png")
        img.save(img_path, "PNG")

        result = ocr.ocr(img_path, cls=True)
        page_text = [line[1][0] for line in result]
        all_text.append("\n".join(page_text))

    return "\n\n".join(all_text)


def main():
    if is_text_pdf(PDF_PATH):
        print("📄 偵測為文字型 PDF，直接抽文字")
        text = extract_text_from_pdf(PDF_PATH)
    else:
        print("🖼 偵測為掃描 PDF，使用 PaddleOCR")
        text = ocr_pdf(PDF_PATH)

    print("\n========== OCR / PDF TEXT ==========\n")
    print(text)


if __name__ == "__main__":
    main()
```

# Qwen3 聊天模組

1. gguf 是「推理用成品模型」
2. safetensors 是「訓練用原始模型」

# GGUF 下載

```
# QWen3 系列
HF_ENDPOINT=https://hf-mirror.com huggingface-cli download bartowski/Qwen_Qwen3-30B-A3B-GGUF --include "*Q5_K_M.gguf" --local-dir ~/Downloads
# LLaMA 系列
HF_ENDPOINT=https://hf-mirror.com huggingface-cli download bartowski/Meta-Llama-3.1-8B-Instruct-GGUF --include "*Q5_K_M.gguf" --local-dir ~/Models

```

# safetensors 下載

```
wget https://hf-mirror.com/hfd/hfd.sh
hfd.sh Qwen/Qwen3-30B-A3B --local-dir /Users/yangfengkai/Downloads/Qwen3-30B-A3B
```

