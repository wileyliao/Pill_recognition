import cv2
import os
import time
from datetime import datetime
import tkinter as tk
from tkinter import Label, Button, Text, Scrollbar
from PIL import Image, ImageTk
import sys

rtsp_url_4k = "rtsp://wiley:82822040@192.168.5.215:554/profile1"

class CameraApp:
    def __init__(self, root, display_size=(1280, 720)):
        self.root = root
        self.root.title("Camera App")
        self.display_size = display_size  # 顯示的縮小尺寸

        # 創建保存資料夾
        self.save_dir = "test_captured"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        # 開啟攝影機 (0 代表預設攝影機)
        self.cap = cv2.VideoCapture(rtsp_url_4k)
        if not self.cap.isOpened():
            self.log("無法開啟攝影機")
            exit()

        # 創建 UI 元素
        self.video_label = Label(self.root)
        self.video_label.pack()

        self.capture_button = Button(self.root, text="拍照", command=self.capture_image)
        self.capture_button.pack(side="left", padx=10, pady=10)

        self.quit_button = Button(self.root, text="退出", command=self.quit)
        self.quit_button.pack(side="right", padx=10, pady=10)

        # 創建終端模擬區域
        self.terminal_text = Text(self.root, height=10, width=50, wrap="word")
        self.terminal_text.pack(padx=10, pady=10)
        self.terminal_text.config(state="disabled")  # 設定為唯讀

        # 重定向終端輸出
        sys.stdout = TextRedirector(self.terminal_text, "stdout")

        # 開始顯示影像
        self.show_frame()

    def show_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.log("無法讀取影像")
            return

        # 原圖尺寸
        original_width, original_height = 3840, 2160
        display_width, display_height = self.display_size
        # [(343, 6), (969, 706)]
        # 計算框在原圖上的位置
        display_x1, display_y1 = 320, 40
        display_x2, display_y2 = 960, 680
        x1 = int(display_x1 * (original_width / display_width))
        y1 = int(display_y1 * (original_height / display_height))
        x2 = int(display_x2 * (original_width / display_width))
        y2 = int(display_y2 * (original_height / display_height))

        # 畫出框（確認框位置）
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 將 OpenCV 影像轉換為 PIL 影像，並縮小尺寸顯示
        cv2_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2_img)
        img = img.resize(self.display_size, Image.LANCZOS)  # 縮小顯示尺寸
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # 定期更新影像
        self.root.after(10, self.show_frame)

    def capture_image(self):
        # 獲取當前影像
        ret, frame = self.cap.read()
        if not ret:
            self.log("無法讀取影像")
            return

        # 調整框的座標至原圖大小
        ratio = 3
        x1, y1 = int(320 * ratio), int(40 * ratio)
        x2, y2 = int(960 * ratio), int(680 * ratio)

        # 儲存影像（保持原始尺寸）
        formatted_time = datetime.now().strftime("%Y-%m-%d_%H_%M_%S_%f")[:-3]  # 截取到毫秒
        filename = fr"{self.save_dir}/{formatted_time}.png"
        cv2.imwrite(filename, frame)
        cv2.imwrite(fr"{self.save_dir}/{formatted_time}_test.png", frame[y1:y2, x1:x2])
        self.log(f"已儲存: {filename}")

    def quit(self):
        self.cap.release()
        self.root.destroy()

    def log(self, message):
        """在終端模擬器中顯示訊息"""
        print(message)

class TextRedirector:
    def __init__(self, text_widget, tag):
        self.text_widget = text_widget
        self.tag = tag

    def write(self, message):
        self.text_widget.config(state="normal")
        self.text_widget.insert("end", message)
        self.text_widget.config(state="disabled")
        self.text_widget.see("end")  # 自動滾動到最後

    def flush(self):
        pass  # 實現需要的 flush 方法


# 啟動應用程式
if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root, display_size=(1280, 720))  # 調整顯示的視窗大小
    root.mainloop()
