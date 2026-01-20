# entities/invoice_parsers.py
INVOICE_PARSERS = {
    "VatElectronicInvoiceFull": {
        # OCR可抓字段
        "Number": r"发票号码[:：]?\s*(\d+)",
        "Date": r"开票日期[:：]?\s*([\d年月日]+)",
        "Buyer": r"购\s*买\s*方\s*信\s*息.*?名称[:：]?\s*([^\n]+)",
        "BuyerTaxID": r"统一社会信用代码/纳税人识别号[:：]?\s*(\w+)",
        "Seller": r"销\s*售\s*方\s*信\s*息.*?名称[:：]?\s*([^\n]+)",
        "SellerTaxID": r"统一社会信用代码/纳税人识别号[:：]?\s*(\w+)",
        "VatElectronicItems.Name": r"\*运输服务\*客运服务费",
        "VatElectronicItems.Price": r"单\s*价\s*([\d.]+)",
        "VatElectronicItems.Quantity": r"数\s*量\s*(\d+)",
        "VatElectronicItems.TaxRate": r"税率/征收率\s*(\d+%)",
        "VatElectronicItems.Tax": r"税\s*额\s*([\d.]+)",
        "VatElectronicItems.Total": r"金\s*额\s*([\d.]+)",
        "TotalCn": r"价税合计（大写）\s*([\u4e00-\u9fa5]+)",
        "Total": r"（小写）\s*¥?([\d.]+)",
        "Issuer": r"开票人[:：]?\s*([^\n]+)",

        # 固定值或默认值
        "CompanySealMark": 0,
        "InvoicePageIndex": "",
        "PretaxAmountMark": "¥",
        "Remark": "",
        "ServiceTypeLabel": "旅客运输服务",
        "SubTax": "",
        "SubTotal": "",
        "TaxMark": "¥",
        "Title": "电子发票(普通发票)",
        "TotalCnMark": "⊗",
        "TotalMark": "¥",
    },
    "ElectronicTrainTicketFull": {
        "Number": r"发票号码[:：]?\s*(\d+)",
        "Date": r"开票日期[:：]?\s*([\d年月日]+)",

        "StationGetOn": r"([\u4e00-\u9fa5]+)站",  # 上车站
        "StationGetOff": r"([\u4e00-\u9fa5]+)站",  # 下车站

        "TrainNumber": r"\n([A-Z]\d+)\n",
        "DateGetOn": r"(\d{4}年\d{2}月\d{2}日)",  # 只抓日期
        "TimeGetOn": r"(\d{2}:\d{2})开",  # 单独抓时间

        "SeatNumber": r"(\d+车\d+[A-Z]号)",
        "Seat": r"(二等座|一等座|特等座)",
        "Fare": r"￥\s*([\d\.]+)",

        "UserID": r"(\d{6,}\*{2,}\d+)",
        "UserName": r"\d{6,}\*{2,}\d+\s*\n([\u4e00-\u9fa5]{2,4})",

        "ElectronicTicketNum": r"电子客票号[:：]?\s*(\d+)",
        #"Buyer": r"购买方名称[:：]?\s*(.+)",
        "Buyer": r"购买方名称[:：]?([^\n]+)",
        "BuyerTaxID": r"统一社会信用代码[:：]?\s*(\d+)",

        "TypeOfVoucher": r"(电子发票（铁路电子客票）)",
    }
    # 其他票種...
}
