import os
from pathlib import Path
from PIL import Image
from paddleocr import PaddleOCR
import multiprocessing

num_cores = os.cpu_count()
print(f"多核 CPU，共 {num_cores} 核")

# PP-OCRv3：超輕量級，速度最快，適合邊緣設備。準確率較低，複雜場景（如手寫、豎排、罕見字）
# PP-OCRv4：準確率明顯提升（尤其文件類文字），支援更多語言/字符（含部分繁中、日文、特殊符號）。分 mobile（輕量）與 server（高精）兩種。整體平衡速度與精度。
# PP-OCRv5（最新）：單模型統一支援簡中、繁中、英文、日文、漢語拼音。對手寫、豎排、罕見字、複雜場景提升最大，端到端準確率比 v4 高約 13%。模型稍大，推理稍慢，但綜合 SOTA 級別。

# 🔹 CPU/GPU 自動初始化 PaddleOCR
# 如果有 GPU，use_gpu=True；否則 CPU 使用 MKL 加速
ocr = PaddleOCR(
    lang="ch",
    use_angle_cls=False,  # 關閉方向檢測，加速
    enable_mkldnn=True,  # CPU 加速
    rec_batch_num=10,  # 文本识别参数
    # 其他优化参数
    det_db_thresh=0.3,
    det_db_box_thresh=0.5,
    det_db_unclip_ratio=1.5,
    ocr_version="PP-OCRv4",
)

IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".tiff"]


def _ocr_single(img_path: Path) -> str:
    """單張圖片 OCR，CPU 最佳化"""
    if not img_path.exists():
        return ""
    # 打開圖片，轉 RGB，縮小，加速 OCR
    img = Image.open(img_path).convert("RGB")
    img.thumbnail((1200, 1200))

    # 轉 numpy array，直接傳給 PaddleOCR
    import numpy as np
    img_np = np.array(img)

    result = ocr.ocr(img_np)  # ✅ 省掉磁碟 I/O
    text_lines = [line[1][0] for line in result]
    return "\n".join(text_lines)


def ocr_images(img_paths: list[Path]) -> str:
    """多張圖片 OCR 支援單張或多張"""
    if len(img_paths) == 1:
        # 單張直接處理
        return _ocr_single(img_paths[0])

    # 🔹 多張圖片使用多線程加速 CPU
    max_workers = min(len(img_paths), multiprocessing.cpu_count())
    from concurrent.futures import ThreadPoolExecutor
    texts = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for text in executor.map(_ocr_single, img_paths):
            texts.append(text)
    return "\n".join(texts).strip()
