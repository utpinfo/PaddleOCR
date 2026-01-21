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
    rec_batch_num=10,  # OCR 識別階段的批次大小（batch size）。預設 6， 值越大：GPU 利用率高、整體速度快，但顯存消耗大。
    # 二值化閾值（像素分數 > 0.3 視為文字區域）。值越低越容易偵測弱文字，但雜訊也多。
    #det_db_thresh=0.3,
    # 文字框分數閾值（框內平均分數 > 0.5 才保留該框）。值越高越嚴格，漏檢率上升。
    #det_db_box_thresh=0.5,
    # 文字框擴張比例（DBNet 後處理時向外膨脹 1.5 倍）。值越大框越鬆，適合彎曲/變形文字；太小會漏邊緣。
    #det_db_unclip_ratio=1.5,
    ocr_version="PP-OCRv4",
)

IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".tiff"]


def _ocr_single(img_path: Path) -> str:
    """單張圖片 OCR，CPU 最佳化，兼容 PP-OCRv3/v4/v5"""
    if not img_path.exists():
        return ""

    img = Image.open(img_path).convert("RGB")
    img.thumbnail((1200, 1200))
    import numpy as np
    img_np = np.array(img)

    result = ocr.ocr(img_np)  # 可直接傳 numpy array

    text_lines = []
    # v4/v5 返回 dict list
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
        text_lines = result[0].get('rec_texts', [])
    else:
        # v3 格式
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
