import cv2
import os
import time
import tkinter as tk
from tkinter import Label, Button, Text, Scrollbar
from PIL import Image, ImageTk
import sys

class CameraApp:
    def __init__(self, root, display_size=(320, 240)):
        self.root = root
        self.root.title("Camera App")
        self.display_size = display_size  # 顯示的縮小尺寸

        # 創建保存資料夾
        self.save_dir = "test_captured"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        # 開啟攝影機 (0 代表預設攝影機)
        self.cap = cv2.VideoCapture(0)
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

        # 畫出框 (綠色邊框，粗細為2)
        cv2.rectangle(frame, (250, 100), (450, 250), (0, 255, 0), 2)

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

        # 儲存影像（保持原始尺寸）
        formatted_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        filename = fr"{self.save_dir}/{formatted_time}.png"
        cv2.imwrite(filename, frame)
        cv2.imwrite(fr"{self.save_dir}/{formatted_time}_test.png", frame[100:250, 250:450])
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
    app = CameraApp(root, display_size=(800, 600))  # 調整顯示的視窗大小
    root.mainloop()
