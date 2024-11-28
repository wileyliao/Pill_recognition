from flask import Flask, request, jsonify
from Pill_base64_utils import *
from Pill_main import pill_recognition_main
from datetime import datetime
import threading
import cv2
import os


def save_image(time, image, subdir="client_capture"):
    # 確保子目錄存在
    os.makedirs(subdir, exist_ok=True)
    # 生成檔案名稱並保存影像
    file_path = os.path.join(subdir, f"{time}.jpg")
    cv2.imwrite(file_path, image)


app = Flask(__name__)

prefix = "data:image/jpeg;base64,"

@app.route('/Pill_recognition', methods=['POST'])
def main():
    try:
        data = request.json['Data'][0]['base64']
        image = base64_decoder(data[len(prefix):])

        if request.json.get('Value'):
            op_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_image_thread = threading.Thread(target=save_image, args=(op_time, image,))
            save_image_thread.start()
            check = f'file_name: {op_time}'
        else:
            check = ""

        result, exe_time = pill_recognition_main(image)

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


if __name__ == "__main__":
    app.run(port=3050, debug=True)