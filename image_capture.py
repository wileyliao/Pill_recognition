import cv2
import os
import time

# 開啟攝影機 (0 代表預設攝影機)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

if not cap.isOpened():
    print("無法開啟攝影機")
    exit()

# 設定框的大小及位置 (960x960，向上平移60像素)
box_size = 960
frame_width, frame_height = 1600, 1200
top_left_x = (frame_width - box_size) // 2
top_left_y = ((frame_height - box_size) // 2) - 60
bottom_right_x = top_left_x + box_size
bottom_right_y = top_left_y + box_size

# 設定曝光度列表
exposures = [-7, -6, -5]
photo_counter = 1  # 初始照片編號

# 創建保存資料夾
save_dir = "captured_images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

while True:
    # 讀取攝影機影像
    ret, frame = cap.read()
    if not ret:
        print("無法讀取影像")
        break

    # 在影像中畫出框 (綠色邊框，粗細為2)
    cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)

    # 顯示影像
    cv2.imshow('Camera Feed', frame)

    # 按下 's' 鍵拍照
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        # 儲存原本的曝光度設定
        original_exposure = cap.get(cv2.CAP_PROP_EXPOSURE)

        for exposure in exposures:
            # 設定不同的曝光度
            cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
            time.sleep(1)  # 等待設定生效

            ret, frame = cap.read()  # 重新讀取影像以應用曝光度

            if not ret:
                print(f"無法讀取影像 (曝光度: {exposure})")
                continue

            # 截取指定框範圍內的影像
            cropped_frame = frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]

            # 儲存影像，檔名依序遞增
            filename = f"{save_dir}/T-R-Confuse_A_0{photo_counter}.jpg"
            cv2.imwrite(filename, cropped_frame)
            print(f"已儲存: {filename}")
            photo_counter += 1

        # 恢復原本的曝光度
        cap.set(cv2.CAP_PROP_EXPOSURE, original_exposure)

    # 按下 'q' 鍵退出
    if key == ord('q'):
        break

# 釋放攝影機並關閉視窗
cap.release()
cv2.destroyAllWindows()
