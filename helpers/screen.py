from PIL import ImageGrab

pytesseract = None
TESSERACT_AVAILABLE = False

def init_tesseract(pytess, available):
    global pytesseract, TESSERACT_AVAILABLE
    pytesseract = pytess
    TESSERACT_AVAILABLE = available


class Screen:
    @staticmethod
    def positionHasColor(x: int, y: int, hex_color: str) -> bool:
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
            pixel = screenshot.getpixel((0, 0))
            current_color = "#{:02X}{:02X}{:02X}".format(pixel[0], pixel[1], pixel[2])
            return current_color.upper() == hex_color.upper()
        except Exception as e:
            print(f"Erro ao verificar cor: {e}")
            return False
    
    @staticmethod
    def positionHasSomeColor(x: int, y: int, colors: list) -> bool:
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
            pixel = screenshot.getpixel((0, 0))
            current_color = "#{:02X}{:02X}{:02X}".format(pixel[0], pixel[1], pixel[2]).upper()
            return any(current_color == c.upper() for c in colors)
        except Exception as e:
            print(f"Erro ao verificar cores: {e}")
            return False
    
    @staticmethod
    def getColorAt(x: int, y: int) -> str:
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
            pixel = screenshot.getpixel((0, 0))
            return "#{:02X}{:02X}{:02X}".format(pixel[0], pixel[1], pixel[2])
        except Exception as e:
            print(f"Erro ao obter cor: {e}")
            return "#000000"
    
    @staticmethod
    def getAreaText(x1: int, y1: int, x2: int, y2: int) -> str:
        if not TESSERACT_AVAILABLE:
            return ""
        try:
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            return pytesseract.image_to_string(screenshot).strip()
        except Exception as e:
            print(f"Erro ao extrair texto: {e}")
            return ""
    
    @staticmethod
    def areaHasText(x1: int, y1: int, x2: int, y2: int, text: str) -> bool:
        try:
            extracted_text = Screen.getAreaText(x1, y1, x2, y2)
            return text.strip().lower() in extracted_text.lower()
        except Exception as e:
            print(f"Erro ao verificar texto: {e}")
            return False
    
    @staticmethod
    def areaHasAtLeastOneText(x1: int, y1: int, x2: int, y2: int, texts: list) -> bool:
        try:
            extracted_text = Screen.getAreaText(x1, y1, x2, y2).lower()
            return any(t.strip().lower() in extracted_text for t in texts)
        except Exception as e:
            print(f"Erro ao verificar textos: {e}")
            return False
    
    @staticmethod
    def areaHasAllTexts(x1: int, y1: int, x2: int, y2: int, texts: list) -> bool:
        try:
            extracted_text = Screen.getAreaText(x1, y1, x2, y2).lower()
            return all(t.strip().lower() in extracted_text for t in texts)
        except Exception as e:
            print(f"Erro ao verificar textos: {e}")
            return False
