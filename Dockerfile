# 版本查詢 (https://hub.docker.com/_/python)
FROM python:3.12.12-slim

# 系統依賴（OpenCV / Paddle 需要）
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Python 套件（經驗證穩定）
RUN pip install --no-cache-dir \
    fastapi uvicorn gunicorn \
    "paddleocr[all]" paddlex[ocr] paddlepaddle \
    pdf2image pdfminer.six pillow \
    rapidfuzz python-multipart bs4 layoutparser

WORKDIR /app


# 容器啟動時預設進入 bash
CMD ["/bin/bash"]