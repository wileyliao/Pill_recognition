from flask import Flask, request, jsonify
from Pill_base64_utils import *
from Pill_main import pill_recognition_main

app = Flask(__name__)

prefix = "data:image/jpeg;base64,"

@app.route('/Pill_recognition', methods=['POST'])
def main():
    try:
        data = request.json['Data'][0]['base64']
        image = base64_decoder(data[len(prefix):])
        result, exe_time = pill_recognition_main(image)

        response_data = {
            'Data': result,
            'Result': f'{exe_time:.2f}秒'
        }

        return jsonify(response_data), 200

    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.run(port=3050)