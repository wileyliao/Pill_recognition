import json

from flask import Flask, request, jsonify
from Pill_base64_utils import *
from Pill_main import pill_recognition_main
from ultralytics import YOLO
from datetime import datetime
import threading
import cv2
import os
from flask_cors import CORS

with open("config.json", "r", encoding="utf-8") as file:
    config_file = json.load(file)


def save_image(time, image, subdir):
    # 確保子目錄存在
    os.makedirs(subdir, exist_ok=True)
    # 生成檔案名稱並保存影像
    file_path = os.path.join(subdir, f"{time}.jpg")
    cv2.imwrite(file_path, image)


app = Flask(__name__)
CORS(app)

prefix = "data:image/jpeg;base64,"

model = YOLO(config_file.get("model_path"))

image_save_path = config_file.get("client_capture")

@app.route('/Pill_recognition', methods=['POST'])
def main():
    try:
        data = request.json['Data'][0]['base64']
        image = base64_decoder(data[len(prefix):])

        if request.json.get('Value'):
            op_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_image_thread = threading.Thread(target=save_image, args=(op_time, image, image_save_path))
            save_image_thread.start()
            check = f'file_name: {op_time}'
        else:
            check = ""

        result, exe_time = pill_recognition_main(image, model)

        response_data = {
            'Data': result,
            'Code': 200,
            'Result': check,
            'TimeTaken': f'{exe_time:.2f}秒'
        }

        return jsonify(response_data), 200

    except Exception as e:
        error_response = {
            'Data': "",
            'Code': -200,
            'Result': f'{e}'
        }
        print(e)
        return jsonify(error_response), -200


@app.route('/Pill_recognition/test', methods=['GET'])
def test_communication():

    response_data = {
        'Message': '數粒辨識 Communication Successful',
        'Code': 200,
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(response_data), 200

if __name__ == "__main__":
    app.run(port=3050, debug=True)