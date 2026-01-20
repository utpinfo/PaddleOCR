# entities/invoice_type.py

from dataclasses import dataclass


@dataclass(frozen=True)
class InvoiceType:
    subtype: str  # 英文票種
    description: str  # 中文名稱
    type_id: int  # 大類


# 靜態票種表
INVOICE_TYPE = {
    "VatSpecialInvoice": ("增值税专用发票", 3),
    "VatCommonInvoice": ("增值税普通发票", 3),
    "VatElectronicCommonInvoice": ("增值税电子普通发票", 3),
    "VatElectronicSpecialInvoice": ("增值税电子专用发票", 3),
    "VatElectronicInvoiceBlockchain": ("区块链电子发票", 3),
    "VatElectronicInvoiceToll": ("增值税电子普通发票(通行费)", 3),
    "VatSalesList": ("增值税销货清单", 3),
    "VatElectronicSpecialInvoiceFull": ("电子发票(专用发票)", 16),
    "VatElectronicInvoiceFull": ("电子发票(普通发票)", 16),
    "ElectronicFlightTicketFull": ("电子发票(机票行程单)", 16),
    "ElectronicTrainTicketFull": ("电子发票(铁路电子客票)", 16),
    "MotorVehicleSaleInvoice": ("机动车销售统一发票", 12),
    "UsedCarPurchaseInvoice": ("二手车销售统一发票", 12),
    "MotorVehicleSaleInvoiceElectronic": ("机动车销售统一发票（电子）", 12),
    "UsedCarPurchaseInvoiceElectronic": ("二手车销售统一发票（电子）", 12),
    "VatInvoiceRoll": ("增值税普通发票(卷票)", 11),
    "TaxiTicket": ("出租车发票", 0),
    "QuotaInvoice": ("定额发票", 1),
    "TrainTicket": ("火车票", 2),
    "AirTransport": ("机票行程单", 5),
    "MachinePrintedInvoice": ("通用机打发票", 8),
    "BusInvoice": ("汽车票", 9),
    "ShippingInvoice": ("轮船票", 10),
    "NonTaxIncomeGeneralBill": ("非税收入通用票据", 15),
    "NonTaxIncomeElectronicBill": ("非税收入一般缴款书(电子)", 15),
    "TollInvoice": ("过路过桥费发票", 13),
    "MedicalOutpatientInvoice": ("医疗门诊收费票据（电子）", 17),
    "MedicalHospitalizedInvoice": ("医疗住院收费票据（电子）", 17),
    "TaxPayment": ("完税凭证", 18),
    "CustomsPaymentReceipt": ("海关缴款", 19),
    "BankSlip": ("银行回单", 20),
    "OnlineTaxiItinerary": ("网约车行程单", 21),
    "CustomsDeclaration": ("海关进/出口货物报关单", 22),
    "OverseasInvoice": ("海外发票", 23),
    "ShoppingReceipt": ("购物小票", 24),
    "SaleInventory": ("销货清单", 25),
    "ElectronicTollSummary": ("通行费电子票据汇总单", 26),
    "OtherInvoice": ("其他发票", -1),
}
