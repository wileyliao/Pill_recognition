import requests
import json
import base64

# 將圖片轉為 Base64 字串（假設圖片路徑為 'image.jpg'）
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        b64_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_string}"


with open("config.json", "r", encoding="utf-8") as file:
    config_file = json.load(file)

# 設定要傳送的 API URL
post_url = config_file.get("local_post_url")  # 替換為您的 API URL
get_url = config_file.get("local_get_url")

# 編碼圖片並建立請求資料格式
image_path = config_file.get("test_image")
base64_string = encode_image_to_base64(image_path)

payload = {
    "Data": [
        {
            "base64": base64_string
        }
    ],
    "Value": "True"
}

# 設定請求標頭
headers = {
    "Content-Type": "application/json"
}

# 發送 POST 請求並等待回傳結果
# response = requests.post(post_url, headers=headers, data=json.dumps(payload))
response = requests.get(get_url)

# 檢查回傳結果
if response.status_code == 200:
    # 解析回傳的 JSON 資料
    response_data = response.json()
    print("回傳資料：", json.dumps(response_data, indent=4, ensure_ascii=False))
else:
    print("API 請求失敗，狀態碼：", response.status_code)