import os
from pathlib import Path

import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
import multiprocessing

import layoutparser as lp

num_cores = os.cpu_count()
print(f"多核 CPU，共 {num_cores} 核")

# ------------------------
# 🔹 初始化 OCR
# ------------------------
ocr = PaddleOCR(
    lang="ch",
    use_angle_cls=True,
    enable_mkldnn=True,
    rec_batch_num=20,
    text_det_box_thresh=0.7,
    text_det_thresh=0.4,
    ocr_version="PP-OCRv4",
)

# ------------------------
# 🔹 LayoutParser 延遲初始化
# ------------------------
_layout_model = None


def get_layout_model():
    """延遲初始化 LayoutParser 模型，避免 uvicorn spawn 問題"""
    global _layout_model
    if _layout_model is None:
        _layout_model = lp.PaddleDetectionLayoutModel(
            model_path="lp://PubLayNet/ppyolov2_r50vd_dcn_365e_publaynet",
            label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"},
            device='cpu',
            extra_config={"score_thresh": 0.5}  # 代替舊版 threshold
        )
    return _layout_model


# ------------------------
# 🔹 支援圖片格式
# ------------------------
IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".tiff"]


# ------------------------
# 🔹 單張 OCR
# ------------------------
def _ocr_single(img_path: Path) -> str:
    if not img_path.exists():
        return ""

    img = Image.open(img_path).convert("RGB")
    img.thumbnail((1200, 1200))
    import numpy as np
    img_np = np.array(img)

    result = ocr.ocr(img_np)

    # v3/v4/v5 兼容
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
        rec_texts = result[0].get('rec_texts', [])
    else:
        rec_texts = [line[1][0] for line in result]

    return "\n".join(rec_texts)


# ------------------------
# 🔹 多圖 OCR
# ------------------------
def ocr_images(img_paths: list[Path]) -> str:
    """支援單張或多張圖片，多圖使用多線程加速"""
    if len(img_paths) == 1:
        return _ocr_single(img_paths[0])

    max_workers = min(len(img_paths), multiprocessing.cpu_count())
    from concurrent.futures import ThreadPoolExecutor
    texts = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for text in executor.map(_ocr_single, img_paths):
            texts.append(text)
    return "\n".join(texts).strip()


# ------------------------
# 🔹 Layout 分析接口
# ------------------------
def layout_analyze(img_path: Path):
    """返回 LayoutParser 的區塊列表"""
    if not img_path.exists():
        return []

    img = Image.open(img_path).convert("RGB")
    img_np = np.array(img)

    model = get_layout_model()
    layout = model.detect(img_np)
    return layout  # LayoutBlock 列表，可進一步操作
