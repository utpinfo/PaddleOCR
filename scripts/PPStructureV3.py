from paddleocr import PPStructureV3
from pathlib import Path
from bs4 import BeautifulSoup
import re
import csv

# 1️⃣ 初始化 PP-StructureV3
pipeline = PPStructureV3(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    ocr_version="PP-OCRv4",
    enable_mkldnn=False,
)

# 2️⃣ OCR 預測
input_path = "/home/yangfk0128/AT260100004950032.png"
output_path = Path("output")
output_path.mkdir(exist_ok=True, parents=True)

output = pipeline.predict(input=input_path)
print("****************************************")
# 3️⃣ 遍歷每頁結果
for page_idx, res in enumerate(output):
    print(f"=== Page {page_idx + 1} ===")

    # c. 解析 parsing_res_list（LayoutBlock 物件）
    parsing_list = res["parsing_res_list"]

    invoice_info = {}
    table_rows_clean = []
    print(parsing_list)
    for block in parsing_list:
        # ⭐ 正確方式：LayoutBlock → dict
        d = block.to_dict()

        label = d["label"]
        content = d["content"]

        # 文字欄位：發票號碼 / 開票日期
        if label == "text":
            if match := re.search(r"发票号码[:：]?\s*(\d+)", content):
                invoice_info["invoice_number"] = match.group(1)

            if match := re.search(r"开票日期[:：]?\s*([\d年月日]+)", content):
                invoice_info["invoice_date"] = match.group(1)
        elif label == "figure_title":
            invoice_info["invoice_title"] = content
        # 表格欄位（HTML）
        elif label == "table" and content:
            soup = BeautifulSoup(content, "html.parser")
            table = soup.find("table")
            if not table:
                continue

            for tr in table.find_all("tr"):
                cells = tr.find_all(["td", "th"])
                row = []

                for cell in cells:
                    colspan = int(cell.get("colspan", 1))
                    text = cell.get_text(strip=True)
                    row.extend([text] * colspan)

                if any(cell for cell in row):
                    table_rows_clean.append(row)

    # 4️⃣ 顯示發票資訊
    print("發票資訊：", invoice_info)

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

    # Debug 預覽
    for row in table_rows_clean:
        print(row)
