import cv2
import pyautogui
import time
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QTimer

rounds = 0
paused = False

class ImageClicker(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create buttons and labels
        self.start_button = QPushButton('Start', self)
        self.stop_button = QPushButton('Stop', self)
        self.rounds_label = QLabel('Rounds: 0', self)

        # Connect buttons to functions
        self.start_button.clicked.connect(self.start_script)
        self.stop_button.clicked.connect(self.stop_script)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.rounds_label)

        self.setLayout(layout)

        # Set up timer for periodic checks
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_images)
        self.timer.start(15000)  # 15 seconds interval

        self.update_ui()

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('BGBOT')
        self.show()

    def start_script(self):
        global paused
        paused = False
        self.update_ui()

    def stop_script(self):
        global paused
        paused = True
        self.update_ui()

    def check_images(self):
        global rounds, paused
        if not paused:
            if click_image_if_found("play-button.png", "Hearthstone.exe"):
                time.sleep(2)
            elif click_image_if_found("rating.png", "Hearthstone.exe"):
                time.sleep(2)
                rounds += 1
                self.update_ui()
            else:
                print("Images not found. Waiting for the next check.")

    def update_ui(self):
        self.start_button.setEnabled(paused)
        self.stop_button.setEnabled(not paused)
        self.rounds_label.setText(f'Rounds: {rounds}')


def find_image_on_screen(image_path):
    screen = pyautogui.screenshot()
    screen.save("screenshot.png")

    screenshot = cv2.imread("screenshot.png")
    template = cv2.imread(image_path)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    return max_val, max_loc


def click_image_if_found(image_path, process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            confidence, location = find_image_on_screen(image_path)

            if confidence > 0.8:
                x, y = location
                pyautogui.click(x, y)
                print(f"Clicked {image_path}")
                return True

    return False


if __name__ == '__main__':
    app = QApplication([])
    window = ImageClicker()
    app.exec_()
