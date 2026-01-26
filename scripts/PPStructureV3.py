from paddleocr import PPStructureV3
from pathlib import Path
from bs4 import BeautifulSoup
import re
import csv

from app.entities.invoice_parsers import INVOICE_PARSERS
from app.entities.invoice_type import INVOICE_TYPE
from app.services.invoice_classifier import classify_invoice

# 1️⃣ 初始化 PP-StructureV3
pipeline = PPStructureV3(
    lang="ch",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    ocr_version="PP-OCRv4",
    enable_mkldnn=True,
    text_det_thresh=0.3,  # 預設 0.3~0.5
    text_det_box_thresh=0.3,
    text_det_unclip_ratio=1.3,  # 預設 1.5
    text_det_limit_side_len=960  # 或 1280
)

# 2️⃣ OCR 預測
input_path = "/home/yangfk0128/AT260100004964081.pdf"
output_path = Path("output")
output_path.mkdir(exist_ok=True, parents=True)

output = pipeline.predict(input=input_path)
print("****************************************")
invoice_type = INVOICE_TYPE
parser = INVOICE_PARSERS["VatElectronicInvoiceFull"]

# 3️⃣ 遍歷每頁結果
for page_idx, res in enumerate(output):
    print(f"=== Page {page_idx + 1} ===")

    # c. 解析 parsing_res_list（LayoutBlock 物件）
    parsing_list = res["parsing_res_list"]

    invoice_info = {}
    table_rows_clean = []
    # print(parsing_list)
    for block in parsing_list:
        # ⭐ 正確方式：LayoutBlock → dict
        d = block.to_dict()

        label = d["label"]
        content = d["content"]

        # 文字欄位：發票號碼 / 開票日期
        if label == "text":
            if match := re.search(r"发票号码[:：]?\s*(\d+)", content):
                invoice_info["invoiceNumber"] = match.group(1)

            if match := re.search(r"开票日期[:：]?\s*([\d年月日]+)", content):
                invoice_info["invoiceDate"] = match.group(1)
        elif label == "figure_title":
            type = classify_invoice(content, threshold=50)
            invoice_info["SubType"] = type["SubType"]
        # 表格欄位（HTML）
        elif label == "table" and content:
            soup = BeautifulSoup(content, "html.parser")
            table = soup.find("table")
            if table:
                for tr in table.find_all("tr"):
                    row = []
                    for cell in tr.find_all(["td", "th"]):
                        text = cell.get_text(strip=True)
                        if not text:
                            continue
                        if text in row:
                            continue
                        row.append(" ".join(text.split()))
                    if row:
                        table_rows_clean.append(row)

    # 4️⃣ 顯示發票資訊
    print("發票資訊：", invoice_info)
    '''
    # 5️⃣ 輸出 CSV
    if table_rows_clean:
        csv_file = output_path / f"invoice_page_{page_idx + 1}.csv"
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow(["发票号码", invoice_info.get("invoice_number", "")])
            writer.writerow(["开票日期", invoice_info.get("invoice_date", "")])
            writer.writerow(["开票標題", invoice_info.get("invoice_title", "")])
            writer.writerow([])

            writer.writerows(table_rows_clean)

        print(f"表格已輸出到: {csv_file}")
    '''
    # Debug 預覽
    for row in table_rows_clean:
        print(row)
