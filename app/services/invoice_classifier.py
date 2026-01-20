# services/invoice_classifier.py
import re
from collections import defaultdict

from rapidfuzz import process

from app.entities.invoice_parsers import INVOICE_PARSERS
from app.entities.invoice_type import INVOICE_TYPE


def normalize_text(text: str) -> str:
    # 去換行
    text = text.replace("\r\n", "\n").replace("\n\n", "\n").strip()
    # 去換空格
    text = text.replace(" ", "")
    # 全形括號轉半形
    text = text.replace("（", "(").replace("）", ")")
    return text


# 相似度 ≥ threshold% 才算成功
def classify_invoice(ocr_text: str, threshold=80):
    ocr_text_norm = normalize_text(ocr_text)

    # 精準匹配
    for subtype, (chinese_name, type_id) in INVOICE_TYPE.items():
        if normalize_text(chinese_name) in ocr_text_norm:
            return {"SubType": subtype, "TypeDescription": chinese_name, "Type": type_id}

    # 模糊匹配 fallback
    choices = [normalize_text(v[0]) for v in INVOICE_TYPE.values()]
    match, score, idx = process.extractOne(ocr_text_norm, choices)
    if score >= threshold:
        subtype = list(INVOICE_TYPE.keys())[idx]
        chinese_name, type_id = INVOICE_TYPE[subtype]
        return {"SubType": subtype, "TypeDescription": chinese_name, "Type": type_id}

    return {"SubType": "OtherInvoice", "TypeDescription": "其他发票", "Type": -1}


def parse_invoice_by_type(ocr_text: str, subtype: str) -> dict:
    ocr_text = normalize_text(ocr_text)
    print("**********************************************************************")
    print(ocr_text)
    print("**********************************************************************")
    rules = INVOICE_PARSERS.get(subtype)
    if not rules:
        return {}

    result = {}
    items = defaultdict(dict)

    for field, pattern in rules.items():
        if isinstance(pattern, str):
            match = re.search(pattern, ocr_text, re.S)
            value = match.group(1).strip() if match and match.groups() else (
                match.group(0) if match else None
            )
        else:
            # pattern不是字符串（固定值），直接赋值
            value = pattern

        if "." in field:
            group, key = field.split(".", 1)
            items[group][key] = value
        else:
            result[field] = value

    # 自动组装 Item 列表
    for group, item in items.items():
        if any(item.values()):
            result[group] = [item]

    return result
