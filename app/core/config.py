from pathlib import Path
import os

from dotenv import load_dotenv

# 專案根目錄
ROOT_DIR = Path(__file__).resolve().parents[2]

# 基本設定
DPI = 300
UPLOAD_DIR = ROOT_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 載入環境變數（只一次）
load_dotenv()

# 模型目錄
MODEL_BASE_DIR = Path(
    os.getenv("MODEL_BASE_DIR", ROOT_DIR / "Models")
).expanduser().resolve()

# 模型路徑
QWEN_GGUF = MODEL_BASE_DIR / "Qwen_Qwen3-30B-A3B-Q5_K_M.gguf"
#LLAMA_GGUF = MODEL_BASE_DIR / "Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf"
LLAMA_GGUF = MODEL_BASE_DIR / "llama-3.2-1b-instruct-q8_0.gguf"
QWEN_TOKENIZER = MODEL_BASE_DIR / "Qwen3-30B-A3B"

# 啟動即檢查（正式環境必備）
if not MODEL_BASE_DIR.exists():
    raise RuntimeError(f"MODEL_BASE_DIR not found: {MODEL_BASE_DIR}")

if not LLAMA_GGUF.exists():
    raise RuntimeError(f"LLAMA model not found: {LLAMA_GGUF}")
