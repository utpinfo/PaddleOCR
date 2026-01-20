from paddleocr import PaddleOCR

# 全域只初始化一次
ocr = PaddleOCR(lang="ch", use_angle_cls=True)

def ocr_image(img_path: str) -> str:
    """單張圖片 OCR"""
    result = ocr.ocr(img_path, cls=True)
    text = [line[1][0] for line in result]
    return "\n".join(text)

def ocr_images(img_paths: list) -> str:
    """多張圖片 OCR → 合併文字"""
    all_text = []
    for img_path in img_paths:
        all_text.append(ocr_image(img_path))
    return "\n\n".join(all_text)
