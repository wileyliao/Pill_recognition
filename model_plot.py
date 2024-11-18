import cv2
from ultralytics import YOLO
from collections import Counter, defaultdict



# 初始化 YOLO 模型
model = YOLO(r"C:\Projects\Pill_recognition\pill_recognition\exp_02\weights\best.pt")

rtsp_url = "rtsp://wiley:82822040@192.168.5.215:554/profile1"


# 開啟攝影機
cap = cv2.VideoCapture(rtsp_url)  # 0 表示默認攝像頭，您可以改成其他攝像頭的編號
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
cap.set(cv2.CAP_PROP_EXPOSURE, -7)


box_size = 960
frame_width, frame_height = 1600, 1200
top_left_x = (frame_width - box_size) // 2
top_left_y = ((frame_height - box_size) // 2) - 60
bottom_right_x = top_left_x + box_size
bottom_right_y = top_left_y + box_size

# 檢查攝影機是否成功開啟
if not cap.isOpened():
    print("無法開啟攝影機")
    exit()

try:
    while True:
        # 讀取攝影機畫面
        ret, frame = cap.read()
        if not ret:
            print("無法擷取影像")
            break

        cropped_frame = frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

        # 調整圖片大小至模型所需的 640x640
        img_rsz = cv2.resize(cropped_frame, (640, 640))
        img_copy = img_rsz.copy()

        # 使用模型進行預測
        results = model.track(img_rsz, conf=0.7)
        for result in results:
            frame = result.orig_img  # 獲取原始影像
            for box in result.boxes.xyxy:  # 獲取框的座標
                x1, y1, x2, y2 = map(int, box)
                # 繪製只包含框的矩形，不顯示標籤
                cv2.rectangle(img_rsz, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)

        # 繪製結果
        # result_img = results[0].plot()

        # 計算偵測到的框的數量
        num_boxes = len(results[0].boxes)

        # class_counts = Counter([box.cls for box in result[0].boxes])

        # 在影像上顯示框的數量
        cv2.putText(img_rsz, f'Pill counter: {num_boxes}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # 計算各類別的數量（使用計數字典）
        # class_counts = defaultdict(int)
        # for box in result[0].boxes:
        #     cls_id = int(box.cls)  # 取得類別 ID
        #     class_counts[cls_id] += 1  # 計算每個類別的出現次數

        # # 顯示計算的類別數量在影像上
        # y_offset = 60  # 顯示文本的初始 y 座標
        # for cls_id, count in class_counts.items():
        #     class_name = model.names[cls_id]  # 取得類別名稱
        #     cv2.putText(result_img, f'{class_name}: {count}', (10, y_offset),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        #     y_offset += 30  # 增加 y 座標以顯示下一行

        # 顯示結果影像
        cv2.imshow('Pill Detection', img_rsz)

        key = cv2.waitKey(1) & 0xFF  # 只呼叫一次 cv2.waitKey

        if key == ord('s'):
            cv2.imwrite('gif_file01.png', img_rsz)
            cv2.imwrite('gif_file02.png', img_copy)

        # 按下 'q' 鍵退出
        elif key == ord('q'):
            break
finally:
    # 釋放攝影機並關閉視窗
    cap.release()
    cv2.destroyAllWindows()
