import customtkinter as ctk
from tkinter import messagebox
import keyboard

from .code_editor import CodeEditor

Lang = None
DocumentationModal = None

def init_lang(lang_class):
    global Lang
    Lang = lang_class

def init_documentation_modal(doc_modal_class):
    global DocumentationModal
    DocumentationModal = doc_modal_class


class ScriptModal(ctk.CTkToplevel):
    def __init__(self, parent, callback, script_data=None):
        super().__init__(parent)
        self.callback = callback
        self.script_data = script_data
        self.result = None
        self.trigger_hotkey = None
        self.waiting_for_hotkey = False
        
        self.title(Lang.t("add_script_title") if script_data is None else Lang.t("edit_script_title"))
        self.geometry("700x650")
        self.resizable(True, True)
        
        self.transient(parent)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        title_frame = ctk.CTkFrame(self)
        title_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(title_frame, text=Lang.t("title_label"), font=("Arial", 14)).grid(row=0, column=0, padx=(10, 5), pady=10)
        self.title_entry = ctk.CTkEntry(title_frame, placeholder_text=Lang.t("title_placeholder"), font=("Arial", 14))
        self.title_entry.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="ew")
        
        trigger_frame = ctk.CTkFrame(self)
        trigger_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(trigger_frame, text=Lang.t("trigger_type"), font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.trigger_type = ctk.StringVar(value="interval")
        
        options_frame = ctk.CTkFrame(trigger_frame, fg_color="transparent")
        options_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        interval_radio = ctk.CTkRadioButton(
            options_frame,
            text=Lang.t("trigger_interval"),
            variable=self.trigger_type,
            value="interval",
            command=self._on_trigger_change
        )
        interval_radio.pack(side="left", padx=(0, 10))
        
        self.ms_entry = ctk.CTkEntry(options_frame, placeholder_text="1000", font=("Arial", 14), width=120)
        self.ms_entry.pack(side="left", padx=(0, 30))
        
        hotkey_radio = ctk.CTkRadioButton(
            options_frame,
            text=Lang.t("trigger_hotkey"),
            variable=self.trigger_type,
            value="hotkey",
            command=self._on_trigger_change
        )
        hotkey_radio.pack(side="left", padx=(0, 10))
        
        self.hotkey_btn = ctk.CTkButton(
            options_frame,
            text=Lang.t("trigger_hotkey_btn"),
            font=("Arial", 12),
            width=120,
            command=self._start_hotkey_capture,
            state="disabled"
        )
        self.hotkey_btn.pack(side="left", padx=(0, 5))
        
        self.hotkey_clear_btn = ctk.CTkButton(
            options_frame,
            text=Lang.t("trigger_hotkey_clear"),
            font=("Arial", 12),
            width=70,
            fg_color="gray",
            command=self._clear_hotkey,
            state="disabled"
        )
        self.hotkey_clear_btn.pack(side="left")
        
        code_frame = ctk.CTkFrame(self)
        code_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        code_frame.grid_columnconfigure(0, weight=1)
        code_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(code_frame, text=Lang.t("code_label"), font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        self.code_editor = CodeEditor(code_frame, width=600, height=300)
        self.code_editor.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=20, pady=20)
        
        ctk.CTkButton(btn_frame, text=Lang.t("cancel"), command=self.destroy, fg_color="gray").pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text=Lang.t("save"), command=self.save).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="?", width=40, command=self._open_docs, fg_color="#3498DB", hover_color="#2980B9").pack(side="left", padx=10)
        
        if script_data:
            self.title_entry.insert(0, script_data.get("title", ""))
            if script_data.get("trigger_hotkey"):
                self.trigger_type.set("hotkey")
                self.trigger_hotkey = script_data.get("trigger_hotkey")
                self.hotkey_btn.configure(text=self.trigger_hotkey, state="normal")
                self.hotkey_clear_btn.configure(state="normal")
                self.ms_entry.configure(state="disabled")
            else:
                self.ms_entry.insert(0, str(script_data.get("interval_ms", "")))
            self.code_editor.set_code(script_data.get("code", ""))
    
    def _on_trigger_change(self):
        if self.trigger_type.get() == "interval":
            self.ms_entry.configure(state="normal")
            self.hotkey_btn.configure(state="disabled")
            self.hotkey_clear_btn.configure(state="disabled")
        else:
            self.ms_entry.configure(state="disabled")
            self.hotkey_btn.configure(state="normal")
            self.hotkey_clear_btn.configure(state="normal")
    
    def _start_hotkey_capture(self):
        if self.waiting_for_hotkey:
            return
        
        self.waiting_for_hotkey = True
        self.hotkey_btn.configure(text=Lang.t("press_key"), fg_color="#E67E22")
        
        def on_key_event(event):
            if not self.waiting_for_hotkey:
                return
            
            modifiers = []
            if keyboard.is_pressed("ctrl"):
                modifiers.append("ctrl")
            if keyboard.is_pressed("alt"):
                modifiers.append("alt")
            if keyboard.is_pressed("shift"):
                modifiers.append("shift")
            
            key = event.name
            if key not in ["ctrl", "alt", "shift", "left ctrl", "right ctrl", "left alt", "right alt", "left shift", "right shift"]:
                if modifiers:
                    self.trigger_hotkey = "+".join(modifiers) + "+" + key
                else:
                    self.trigger_hotkey = key
                
                self.waiting_for_hotkey = False
                self.hotkey_btn.configure(
                    text=self.trigger_hotkey,
                    fg_color=["#3B8ED0", "#1F6AA5"]
                )
                keyboard.unhook(hook)
        
        hook = keyboard.on_press(on_key_event)
    
    def _clear_hotkey(self):
        self.trigger_hotkey = None
        self.hotkey_btn.configure(text=Lang.t("trigger_hotkey_btn"))
    
    def _open_docs(self):
        if DocumentationModal:
            DocumentationModal(self)
    
    def _validate_syntax(self, code):
        try:
            compile(code, "<string>", "exec")
            return True, None
        except SyntaxError as e:
            return False, f"Line {e.lineno}: {e.msg}"
    
    def save(self):
        title = self.title_entry.get().strip()
        code = self.code_editor.get("1.0", "end-1c")
        
        if not title:
            messagebox.showerror(Lang.t("error"), Lang.t("title_required"))
            return
        
        if self.trigger_type.get() == "interval":
            interval = self.ms_entry.get().strip()
            if not interval.isdigit():
                messagebox.showerror(Lang.t("error"), Lang.t("interval_must_be_number"))
                return
            interval_ms = int(interval)
            trigger_hotkey = None
        else:
            if not self.trigger_hotkey:
                messagebox.showerror(Lang.t("error"), Lang.t("trigger_required"))
                return
            interval_ms = 0
            trigger_hotkey = self.trigger_hotkey
        
        is_valid, error_msg = self._validate_syntax(code)
        if not is_valid:
            messagebox.showerror(Lang.t("syntax_error"), f"{Lang.t('syntax_error_msg')}\n{error_msg}")
            return
        
        self.result = {
            "title": title,
            "interval_ms": interval_ms,
            "trigger_hotkey": trigger_hotkey,
            "code": code,
            "enabled": self.script_data.get("enabled", False) if self.script_data else False
        }
        
        self.callback(self.result, self.script_data)
        self.destroy()
