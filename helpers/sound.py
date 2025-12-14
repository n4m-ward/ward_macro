import ctypes


class Sound:
    @staticmethod
    def beep(frequency: int = 1000, duration: int = 200):
        ctypes.windll.kernel32.Beep(frequency, duration)
