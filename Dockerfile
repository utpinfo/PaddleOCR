FROM python:3.10-slim

# 系統依賴（OpenCV / Paddle 需要）
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Python 套件（經驗證穩定）
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    paddlepaddle==3.2.0 \
    paddleocr \
    paddlex \
    pandas==2.1.4

WORKDIR /app
