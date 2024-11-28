import cv2
import json
import time
from ultralytics import YOLO
from collections import defaultdict


# 初始化 YOLO 模型
model = YOLO(r"C:\python\pytorch\Pill_recognition\exp_05.pt")
# 取得類別名稱對應表
class_names = model.names

def pill_recognition_main(image):
    start_time = time.time()
    # 調整圖片大小至模型所需的 640x640
    img_rsz = cv2.resize(image, (640, 640))
    rsz_factor = 960/640

    data_group = defaultdict(lambda: {
        "name": "undefined",
        "type": "",
        "qty": 0,
        "value": []
    })

    # 使用模型進行預測
    results = model(img_rsz, conf=0.7)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls)  # 類別 ID
            class_name = class_names[cls_id]
            conf = float(box.conf)
            coords_rsz = box.xyxy.cpu().numpy()
            coords_origin = coords_rsz * rsz_factor# 將 CUDA Tensor 移到 CPU 再轉換為 NumPy

            x_min, y_min, x_max, y_max = coords_origin[0]
            # 計算高度和寬度
            height = y_max - y_min
            width = x_max - x_min

            # 計算中心點座標
            center_x = (x_min + x_max) / 2
            center_y = (y_min + y_max) / 2

            # 將資料整理到字典中
            coord_dict = {
                "conf": str(round(conf, 2)),
                "height": str(int(height)),  # 高度
                "width": str(int(width)),  # 寬度
                "center": f"{center_x:.1f},{center_y:.1f}"  # 中心點
            }

            # 初始化類別組
            if data_group[class_name]["type"] == "":
                data_group[class_name]["type"] = class_name

            # 增加該類別的數量與詳細數據
            data_group[class_name]["qty"] = str(int(data_group[class_name]["qty"]) + 1)
            data_group[class_name]["value"].append(coord_dict)

    # 將結果轉換為列表結構
    output_dict = list(data_group.values())

    # 整理到輸出字典

    json_output = json.dumps(output_dict, indent=4, ensure_ascii=False)
    end_time = time.time()
    print(json_output)

    return output_dict, end_time - start_time

if __name__=='__main__':
    image_path_01 = 'captured_images/C_Confuse_A_019.jpg'
    image_path_02 = 'captured_images/T_R_MA_022.jpg'

    img = cv2.imread(image_path_01)
    pill_recognition_main(img)
