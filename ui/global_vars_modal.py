import customtkinter as ctk
from tkinter import messagebox

from .code_editor import CodeEditor

Lang = None

def init_lang(lang_class):
    global Lang
    Lang = lang_class


class GlobalVarsModal(ctk.CTkToplevel):
    def __init__(self, parent, callback, global_vars_code=""):
        super().__init__(parent)
        self.callback = callback
        
        self.title(Lang.t("global_vars_title"))
        self.geometry("700x500")
        self.resizable(True, True)
        
        self.transient(parent)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        info_label = ctk.CTkLabel(
            self, 
            text=Lang.t("global_vars_info"),
            font=("Arial", 12),
            text_color="gray"
        )
        info_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        code_frame = ctk.CTkFrame(self)
        code_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        code_frame.grid_columnconfigure(0, weight=1)
        code_frame.grid_rowconfigure(0, weight=1)
        
        self.code_editor = CodeEditor(code_frame, width=600, height=300)
        self.code_editor.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        if global_vars_code:
            self.code_editor.set_code(global_vars_code)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=20, pady=20)
        
        ctk.CTkButton(btn_frame, text=Lang.t("cancel"), command=self.destroy, fg_color="gray").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text=Lang.t("save"), command=self.save).pack(side="left", padx=10)
    
    def _validate_syntax(self, code):
        try:
            compile(code, "<string>", "exec")
            return True, None
        except SyntaxError as e:
            return False, f"Line {e.lineno}: {e.msg}"
    
    def save(self):
        code = self.code_editor.get("1.0", "end-1c")
        
        if code.strip():
            is_valid, error_msg = self._validate_syntax(code)
            if not is_valid:
                messagebox.showerror(Lang.t("syntax_error"), f"{Lang.t('syntax_error_msg')}\n{error_msg}")
                return
        
        self.callback(code)
        self.destroy()
