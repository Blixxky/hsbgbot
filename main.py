import cv2
import pyautogui
import time
import psutil

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

            if confidence > 0.8:  # Adjust confidence threshold as needed
                x, y = location
                pyautogui.click(x, y)
                print(f"Clicked {image_path}")
                return True

    return False

def main():
    while True:
        if click_image_if_found("play-button.png", "Hearthstone.exe"):
            time.sleep(2)  # Adjust the delay between clicks if needed
        elif click_image_if_found("rating.png", "Hearthstone.exe"):
            time.sleep(2)  # Adjust the delay between clicks if needed
        else:
            print("Images not found. Waiting for the next check.")

        time.sleep(15)

if __name__ == "__main__":
    main()