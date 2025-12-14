import pyautogui


class Keyboard:
    @staticmethod
    def sendKey(key: str):
        pyautogui.press(key)
    
    @staticmethod
    def hotkey(*keys):
        pyautogui.hotkey(*keys)
    
    @staticmethod
    def typeText(text: str, interval: float = 0.0):
        pyautogui.typewrite(text, interval=interval)
