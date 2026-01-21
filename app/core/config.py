from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

DPI = 300
UPLOAD_DIR = ROOT_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
