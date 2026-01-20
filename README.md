🏆 3. PaddleOCR — 中文/高精度場景最強

# 項目結構
ocr-api/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── api/
│   │   ├── __init__.py
│   │   └── ocr.py            # /ocr/image, /ocr/pdf
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # 環境設定
│   │   └── logger.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ocr_service.py    # PaddleOCR 邏輯
│   │   └── pdf_service.py    # pdf2image / pdfminer
│   ├── models/
│   │   └── response.py       # Pydantic response model
│   └── utils/
│       └── file_utils.py
├── scripts/
│   └── test_api.py      # 用 requests 測試 API
├── requirements.txt
├── Dockerfile
└── README.md


# 啟動方式（配合目錄）
uvicorn app.main:app --host 0.0.0.0 --port 8000


# 測試
http://127.0.0.1:8000/api/ocr/run

# congiguration配置
module <- uvicorn
scripts <- app.main:app --host 0.0.0.0 --port 8000 --reload