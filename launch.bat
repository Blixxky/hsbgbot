@echo off

rem Step 1: Create Python 3.11 virtual environment
python -m venv BGBOT

rem Step 2: Activate the virtual environment
call BGBOT\Scripts\activate

rem Step 3: Install required dependencies
pip install opencv-python pyautogui psutil pyqt5

rem Step 4: Run the main.py script
python main.py

rem Step 5: Deactivate the virtual environment
deactivate
