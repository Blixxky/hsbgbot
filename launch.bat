@echo off

python -m venv %~dp0\BGBOT
call %~dp0\BGBOT\Scripts\activate
pip install opencv-python pyautogui psutil 
python %~dp0\main.py
deactivate
