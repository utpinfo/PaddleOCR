🏆 3. PaddleOCR — 中文/高精度場景最強

# 項目結構
```
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
```
## 啟動API

```shell
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8001
# uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## 開機自動啟動

```shell
sudo systemctl daemon-reload
sudo systemctl enable paddleocr-api.service  # 開機自動啟動
sudo systemctl start paddleocr-api.service   # 立即啟動
```

## 自動文件

```shell
cat << EFO > /etc/systemd/system/paddleocr-api.service
[Unit]
Description=PaddleOCR FastAPI Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/PaddleOCR
Environment="PATH=/opt/PaddleOCR/.venv/bin:/usr/bin:/bin"
ExecStart=/root/.pyenv/versions/3.12.11/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8001
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EFO
```


# 啟動方式（配合目錄）
uvicorn app.main:app --host 0.0.0.0 --port 8001


# 測試
```shell
curl -X POST "http://192.168.201.24:8001/api/ocr/upload_pdf" \
  -F "file=@/Users/yangfengkai/Downloads/AT260100004964081.pdf"
```

# PyCharm配置 (congiguration)
module <- uvicorn
scripts <- app.main:app --host 0.0.0.0 --port 8001 --reload