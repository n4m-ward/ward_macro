import pyautogui


class Mouse:
    @staticmethod
    def leftClick(x: int, y: int):
        pyautogui.click(x, y, button='left')
    
    @staticmethod
    def middleClick(x: int, y: int):
        pyautogui.click(x, y, button='middle')
    
    @staticmethod
    def rightClick(x: int, y: int):
        pyautogui.click(x, y, button='right')
    
    @staticmethod
    def moveTo(x: int, y: int):
        pyautogui.moveTo(x, y)
    
    @staticmethod
    def doubleClick(x: int, y: int):
        pyautogui.doubleClick(x, y)
