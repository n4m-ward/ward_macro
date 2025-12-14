import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
import customtkinter as ctk

Lang = None

def init_lang(lang_class):
    global Lang
    Lang = lang_class


class LogManager:
    _instance = None
    _log_frame = None
    _logs_enabled = False
    
    @classmethod
    def set_log_frame(cls, frame):
        cls._log_frame = frame
    
    @classmethod
    def set_enabled(cls, enabled):
        cls._logs_enabled = enabled
    
    @classmethod
    def is_enabled(cls):
        return cls._logs_enabled
    
    @classmethod
    def add_color_log(cls, x: int, y: int, hex_color: str):
        if not cls._logs_enabled or not cls._log_frame:
            return
        
        try:
            log_item = ctk.CTkFrame(cls._log_frame)
            log_item.pack(fill="x", padx=5, pady=2)
            
            color_box = ctk.CTkFrame(log_item, width=20, height=20, fg_color=hex_color)
            color_box.pack(side="left", padx=(5, 10))
            color_box.pack_propagate(False)
            
            text_label = ctk.CTkLabel(log_item, text=f"({x}, {y}) - {hex_color}", font=("Consolas", 11))
            text_label.pack(side="left", padx=5)
            
            def copy_to_clipboard():
                cls._log_frame.clipboard_clear()
                cls._log_frame.clipboard_append(hex_color)
            
            copy_btn = ctk.CTkButton(log_item, text=Lang.t("copy"), width=60, height=24, command=copy_to_clipboard)
            copy_btn.pack(side="right", padx=5)
        except:
            pass
    
    @classmethod
    def add_text_log(cls, text: str):
        if not cls._logs_enabled or not cls._log_frame:
            return
        
        try:
            log_item = ctk.CTkFrame(cls._log_frame)
            log_item.pack(fill="x", padx=5, pady=2)
            
            text_label = ctk.CTkLabel(log_item, text=text, font=("Consolas", 11), anchor="w")
            text_label.pack(side="left", padx=10, fill="x", expand=True)
        except:
            pass


class Debugger:
    _seen_colors = {}
    
    @staticmethod
    def debugColor(x: int, y: int):
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
            pixel = screenshot.getpixel((0, 0))
            hex_color = "#{:02X}{:02X}{:02X}".format(pixel[0], pixel[1], pixel[2])
            
            position_key = f"{x},{y}"
            if position_key not in Debugger._seen_colors:
                Debugger._seen_colors[position_key] = set()
            
            if hex_color in Debugger._seen_colors[position_key]:
                return
            
            Debugger._seen_colors[position_key].add(hex_color)
            
            LogManager.add_color_log(x, y, hex_color)
            
            debug_window = tk.Toplevel()
            debug_window.title(Lang.t("debug_color_title"))
            debug_window.geometry("300x180")
            debug_window.resizable(False, False)
            debug_window.attributes('-topmost', True)
            
            color_frame = tk.Frame(debug_window, bg=hex_color, width=60, height=60)
            color_frame.pack(pady=10)
            color_frame.pack_propagate(False)
            
            info_label = tk.Label(
                debug_window, 
                text=f"{Lang.t('position')} ({x}, {y})\n{Lang.t('color')} {hex_color}",
                font=("Arial", 12)
            )
            info_label.pack(pady=5)
            
            def copy_color():
                debug_window.clipboard_clear()
                debug_window.clipboard_append(hex_color)
                copy_btn.config(text=Lang.t("copied"))
                debug_window.after(1000, lambda: copy_btn.config(text=Lang.t("copy_color")))
            
            copy_btn = tk.Button(debug_window, text=Lang.t("copy_color"), command=copy_color)
            copy_btn.pack(pady=5)
            
        except Exception as e:
            print(f"Erro no debug: {e}")
            messagebox.showerror(Lang.t("error"), f"Erro ao capturar cor: {e}")
    
    @staticmethod
    def printText(text: str, show_alert: bool = False):
        LogManager.add_text_log(text)
        
        if show_alert:
            messagebox.showinfo(Lang.t("debug"), text)
