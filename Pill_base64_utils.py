import base64
import cv2
import numpy as np


def base64_decoder(image_64):
    decode = base64.b64decode(image_64)
    image_array = np.frombuffer(decode, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


def image_to_base64(image_path):
    # 讀取圖片並轉換為 Base64 字串
    with open(image_path, "rb") as image_file:
        # 將圖片內容編碼為 Base64
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_string