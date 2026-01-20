from copy import deepcopy
from uuid import uuid4

from app.entities.invoice_type import INVOICE_TYPE

def build_response_json(ocr_text, invoice_data, page=1):
    """
    ocr_text: OCR文字 (可以忽略或放在需要的欄位)
    invoice_data: classify_invoice 返回的字典 {"SubType", "TypeDescription", "Type"}
    """
    # 建立空的 SingleInvoiceInfos
    single_invoice_infos = {key: None for key in INVOICE_TYPE}

    # 如果分類成功，填充對應票種
    subtype = invoice_data["SubType"]
    single_invoice_infos[subtype] = {
        # 這裡示範一些基本欄位，可根據 OCR 再填充 Buyer, Seller, Total...
        "Title": invoice_data["TypeDescription"],
        "Buyer": "",  # 後面可用 OCR 擷取
        "Seller": "",
        "Total": "",
        "VatElectronicItems": []  # 如果是電子發票，可再填明細
    }

    response = {
        "Response": {
            "MixedInvoiceItems": [
                {
                    "Code": "OK",
                    "Type": invoice_data["Type"],
                    "SubType": invoice_data["SubType"],
                    "TypeDescription": invoice_data["TypeDescription"],  # 總類中文名
                    "SubTypeDescription": invoice_data["TypeDescription"],  # 子票種中文名
                    "Polygon": {  # 先給默認值
                        "LeftBottom": {"X": 0, "Y": 1018},
                        "LeftTop": {"X": 0, "Y": 0},
                        "RightBottom": {"X": 1188, "Y": 1018},
                        "RightTop": {"X": 1188, "Y": 0},
                    },
                    "Angle": 0.0,
                    "SingleInvoiceInfos": single_invoice_infos,
                    "Page": page,
                    "CutImage": "",
                    "ItemPolygon": [],
                    "QRCode": "",
                    "InvoiceSealInfo": {
                        "CompanySealMark": "0",
                        "SupervisionSealMark": "0",
                        "CompanySealMarkInfo": [],
                        "SupervisionSealMarkInfo": []
                    }
                }
            ],
            "RequestId": str(uuid4()),
            "TotalPDFCount": 1
        }
    }

    return response
