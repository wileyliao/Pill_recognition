import cv2


rtsp_url = "rtsp://wiley:82822040@192.168.5.215:554/profile2"


class RectangleDrawer:
    def __init__(self, video_source = rtsp_url):
        self.cap = cv2.VideoCapture(video_source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.rect = []
        self.drawing = False

        if not self.cap.isOpened():
            raise ValueError(f"Failed to open video source {video_source}")

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # 滑鼠按下左鍵
            self.rect = [(x, y)]  # 紀錄起始位置
            self.drawing = True
        elif event == cv2.EVENT_MOUSEMOVE:  # 滑鼠移動
            if self.drawing:
                _, frame = self.cap.read()  # 取得最新的幀
                img_copy = frame.copy()
                cv2.rectangle(img_copy, self.rect[0], (x, y), (0, 255, 0), 2)
                cv2.imshow("Video Stream", img_copy)
        elif event == cv2.EVENT_LBUTTONUP:  # 滑鼠鬆開左鍵
            self.rect.append((x, y))  # 紀錄終止點
            self.drawing = False
            _, frame = self.cap.read()  # 取得最新的幀
            cv2.rectangle(frame, self.rect[0], self.rect[1], (0, 255, 0), 2)
            cv2.imshow("Video Stream", frame)
            print(f"Selected Rectangle Coordinates: {self.rect}")

    def start_drawing(self):
        cv2.namedWindow("Video Stream")
        cv2.setMouseCallback("Video Stream", self.draw_rectangle)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            cv2.imshow("Video Stream", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # 按下 ESC 退出
                break

        self.cap.release()
        cv2.destroyAllWindows()

# 使用示例
if __name__ == "__main__":
    drawer = RectangleDrawer()  # 使用預設攝影機
    drawer.start_drawing()
