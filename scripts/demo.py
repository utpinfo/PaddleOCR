import requests

url = "http://127.0.0.1:8000/api/ocr/upload_pdf"
files = {"file": open("/Users/yangfengkai/Downloads/AT260100004964022.pdf", "rb")}  # 相對路徑
# files = {"file": open("/Users/yangfengkai/Downloads/AT260100004964004.pdf", "rb")}  # 相對路徑

resp = requests.post(url, files=files)
print("Status code:", resp.status_code)
print("Response text:", resp.text)
data = resp.json()

print(data)