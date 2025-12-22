import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import os
import threading
import time
import win32gui
import win32process
import psutil
import pyautogui
import keyboard
from PIL import ImageGrab
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token

from helpers import Screen, Keyboard, Mouse, Sound, Debugger, LogManager
from helpers.screen import init_tesseract
from helpers.debugger import init_lang as init_lang_debugger

pytesseract = None
TESSERACT_AVAILABLE = False
TESSERACT_DOWNLOAD_URL = "https://github.com/UB-Mannheim/tesseract/wiki"

CONFIG_DIR = "C:\\WardMacro"
PROFILES_DIR = os.path.join(CONFIG_DIR, "profiles")
PROFILES_FILE = os.path.join(CONFIG_DIR, "profiles.json")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")
DEFAULT_PROFILE = "default"
DEFAULT_LANGUAGE = "pt"

TRANSLATIONS = {
    "pt": {
        "app_title": "Ward Macro",
        "application": "Aplicação:",
        "enable_logs": "Ativar Logs",
        "profile": "Perfil:",
        "new_profile_placeholder": "Novo perfil...",
        "hotkey_toggle": "Hotkey Pausar/Iniciar:",
        "screen_capture": "Captura de Tela",
        "coordinates": "Coordenadas:",
        "color": "Cor:",
        "hotkey": "Hotkey:",
        "area_capture_ocr": "Captura de Área (OCR):",
        "area": "Área:",
        "select_area": "Selecionar Área",
        "add_script": "+ Adicionar Script",
        "global_vars": "⚙ Variáveis Globais",
        "start": "▶ Iniciar",
        "stop": "⏹ Parar",
        "scripts": "Scripts",
        "logs": "Logs",
        "clear": "Limpar",
        "clear_color_cache": "Limpar Cache de Cores",
        "edit": "Editar",
        "delete": "Excluir",
        "cancel": "Cancelar",
        "save": "Salvar",
        "close": "Fechar",
        "copied": "Copiado!",
        "press_key": "Pressione uma tecla...",
        "add_script_title": "Adicionar Script",
        "edit_script_title": "Editar Script",
        "title_label": "Título:",
        "title_placeholder": "Nome do script",
        "interval_label": "Intervalo (ms):",
        "code_label": "Código Python:",
        "global_vars_title": "Variáveis Globais",
        "global_vars_info": "Defina variáveis globais que estarão disponíveis em todos os scripts.\nExemplo: minha_var = 123",
        "docs_title": "Documentação - Helpers",
        "search": "Buscar:",
        "next": "Próximo",
        "previous": "Anterior",
        "not_found": "Não encontrado",
        "settings": "Configurações",
        "language": "Idioma",
        "portuguese": "Português",
        "english": "English",
        "warning": "Aviso",
        "error": "Erro",
        "success": "Sucesso",
        "confirm": "Confirmar",
        "no_active_script": "Nenhum script ativo para executar!",
        "title_required": "O título é obrigatório!",
        "interval_must_be_number": "O intervalo deve ser um número!",
        "syntax_error": "Erro de Sintaxe",
        "syntax_error_msg": "O código contém erro de sintaxe:",
        "profile_name_required": "Digite um nome para o novo perfil.",
        "profile_exists": "Já existe um perfil com esse nome.",
        "profile_created": "Perfil '{name}' criado com sucesso!",
        "cannot_rename_default": "Não é possível renomear o perfil padrão.",
        "new_name_required": "Digite o novo nome no campo de texto.",
        "profile_renamed": "Perfil renomeado para '{name}'!",
        "cannot_delete_default": "Não é possível excluir o perfil padrão.",
        "confirm_delete_profile": "Deseja excluir o perfil '{name}'?",
        "profile_deleted": "Perfil excluído!",
        "confirm_delete_script": "Deseja excluir o script '{name}'?",
        "save_error": "Não foi possível salvar os scripts:",
        "drag_to_select": "Arraste para selecionar a área. ESC para cancelar.",
        "debug_color_title": "Debug Color",
        "position": "Posição:",
        "copy_color": "Copiar Cor",
        "copy": "Copiar",
        "debug": "Debug",
        "tesseract_not_found_title": "Tesseract não encontrado",
        "tesseract_not_found_msg": "O Tesseract OCR não está instalado ou não foi encontrado.\n\nAs funções de reconhecimento de texto (OCR) não funcionarão.\n\nPara instalar, acesse:\n{url}\n\nApós instalar, reinicie o aplicativo.",
        "language_changed": "Idioma alterado para Português. Reinicie o aplicativo para aplicar as mudanças.",
        "trigger_type": "Tipo de Execução:",
        "trigger_interval": "Intervalo (ms)",
        "trigger_hotkey": "Ao pressionar tecla",
        "trigger_hotkey_btn": "Definir Tecla",
        "trigger_hotkey_clear": "Limpar",
        "trigger_hotkey_none": "Nenhuma tecla definida",
        "trigger_required": "Defina um intervalo ou uma tecla de ativação!",
    },
    "en": {
        "app_title": "Ward Macro",
        "application": "Application:",
        "enable_logs": "Enable Logs",
        "profile": "Profile:",
        "new_profile_placeholder": "New profile...",
        "hotkey_toggle": "Hotkey Pause/Start:",
        "screen_capture": "Screen Capture",
        "coordinates": "Coordinates:",
        "color": "Color:",
        "hotkey": "Hotkey:",
        "area_capture_ocr": "Area Capture (OCR):",
        "area": "Area:",
        "select_area": "Select Area",
        "add_script": "+ Add Script",
        "global_vars": "⚙ Global Variables",
        "start": "▶ Start",
        "stop": "⏹ Stop",
        "scripts": "Scripts",
        "logs": "Logs",
        "clear": "Clear",
        "clear_color_cache": "Clear Color Cache",
        "edit": "Edit",
        "delete": "Delete",
        "cancel": "Cancel",
        "save": "Save",
        "close": "Close",
        "copied": "Copied!",
        "press_key": "Press a key...",
        "add_script_title": "Add Script",
        "edit_script_title": "Edit Script",
        "title_label": "Title:",
        "title_placeholder": "Script name",
        "interval_label": "Interval (ms):",
        "code_label": "Python Code:",
        "global_vars_title": "Global Variables",
        "global_vars_info": "Define global variables that will be available in all scripts.\nExample: my_var = 123",
        "docs_title": "Documentation - Helpers",
        "search": "Search:",
        "next": "Next",
        "previous": "Previous",
        "not_found": "Not found",
        "settings": "Settings",
        "language": "Language",
        "portuguese": "Português",
        "english": "English",
        "warning": "Warning",
        "error": "Error",
        "success": "Success",
        "confirm": "Confirm",
        "no_active_script": "No active script to run!",
        "title_required": "Title is required!",
        "interval_must_be_number": "Interval must be a number!",
        "syntax_error": "Syntax Error",
        "syntax_error_msg": "The code contains a syntax error:",
        "profile_name_required": "Enter a name for the new profile.",
        "profile_exists": "A profile with this name already exists.",
        "profile_created": "Profile '{name}' created successfully!",
        "cannot_rename_default": "Cannot rename the default profile.",
        "new_name_required": "Enter the new name in the text field.",
        "profile_renamed": "Profile renamed to '{name}'!",
        "cannot_delete_default": "Cannot delete the default profile.",
        "confirm_delete_profile": "Do you want to delete the profile '{name}'?",
        "profile_deleted": "Profile deleted!",
        "confirm_delete_script": "Do you want to delete the script '{name}'?",
        "save_error": "Could not save scripts:",
        "drag_to_select": "Drag to select area. ESC to cancel.",
        "debug_color_title": "Debug Color",
        "position": "Position:",
        "copy_color": "Copy Color",
        "copy": "Copy",
        "debug": "Debug",
        "tesseract_not_found_title": "Tesseract not found",
        "tesseract_not_found_msg": "Tesseract OCR is not installed or was not found.\n\nText recognition (OCR) functions will not work.\n\nTo install, visit:\n{url}\n\nAfter installing, restart the application.",
        "language_changed": "Language changed to English. Restart the application to apply changes.",
        "trigger_type": "Trigger Type:",
        "trigger_interval": "Interval (ms)",
        "trigger_hotkey": "On key press",
        "trigger_hotkey_btn": "Set Key",
        "trigger_hotkey_clear": "Clear",
        "trigger_hotkey_none": "No key set",
        "trigger_required": "Set an interval or a trigger key!",
    }
}

class Lang:
    _current = DEFAULT_LANGUAGE
    
    @classmethod
    def set(cls, lang):
        if lang in TRANSLATIONS:
            cls._current = lang
    
    @classmethod
    def get(cls):
        return cls._current
    
    @classmethod
    def t(cls, key):
        return TRANSLATIONS.get(cls._current, TRANSLATIONS[DEFAULT_LANGUAGE]).get(key, key)

def _load_language():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                Lang.set(data.get("language", DEFAULT_LANGUAGE))
        except:
            pass

def _save_language(lang):
    try:
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({"language": lang}, f, indent=2)
    except:
        pass

_load_language()
init_lang_debugger(Lang)

from ui.area_selector import AreaSelector, init_lang as init_lang_area
from ui.script_modal import ScriptModal, init_lang as init_lang_script, init_documentation_modal
from ui.global_vars_modal import GlobalVarsModal, init_lang as init_lang_global
from ui.documentation_modal import DocumentationModal, init_lang as init_lang_docs
from ui.script_item import ScriptItem, init_lang as init_lang_item

init_lang_area(Lang)
init_lang_script(Lang)
init_lang_global(Lang)
init_lang_docs(Lang)
init_lang_item(Lang)
init_documentation_modal(DocumentationModal)

def _init_tesseract():
    global pytesseract, TESSERACT_AVAILABLE
    
    try:
        import pytesseract as _pytesseract
        pytesseract = _pytesseract
        
        tesseract_path = _get_tesseract_path()
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            TESSERACT_AVAILABLE = True
        else:
            TESSERACT_AVAILABLE = False
    except ImportError:
        pytesseract = None
        TESSERACT_AVAILABLE = False
    
    init_tesseract(pytesseract, TESSERACT_AVAILABLE)

def _get_tesseract_path():
    default_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tesseract-OCR", "tesseract.exe")
    ]
    
    for path in default_paths:
        if os.path.exists(path):
            return path
    
    return None

def _check_tesseract_available():
    if not TESSERACT_AVAILABLE:
        messagebox.showerror(
            Lang.t("tesseract_not_found_title"),
            Lang.t("tesseract_not_found_msg").format(url=TESSERACT_DOWNLOAD_URL)
        )
        return False
    return True

_init_tesseract()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def focus_window_by_title(window_title: str) -> bool:
    def callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title and window_title in title:
                results.append(hwnd)
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    if windows:
        hwnd = windows[0]
        try:
            win32gui.SetForegroundWindow(hwnd)
            return True
        except:
            pass
    return False


# UI classes imported from ui/ package
# ScriptModal, GlobalVarsModal, DocumentationModal, ScriptItem, AreaSelector, CodeEditor


class WardMacroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(Lang.t("app_title"))
        self.geometry("900x700")
        self.minsize(700, 500)
        self.attributes('-topmost', False)
        
        self.scripts = []
        self.script_widgets = []
        self.is_running = False
        self.script_threads = []
        self.script_stop_events = []
        self.script_executing = {}
        
        self.current_hotkey = "ctrl+f12"
        self.toggle_hotkey = "f6"
        self.waiting_for_hotkey = False
        self.waiting_for_toggle_hotkey = False
        self.captured_coords = None
        self.captured_color = None
        self.captured_area_start = None
        self.captured_area_end = None
        self.selected_app_title = None
        self.logs_enabled = False
        self.global_vars_code = ""
        self.current_profile = DEFAULT_PROFILE
        self.profiles_list = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        
        self._ensure_config_dir()
        self._load_profiles_config()
        
        self._create_menu()
        self._create_header()
        self._create_profile_section()
        self._create_picker_section()
        self._create_add_button()
        self._create_scripts_list()
        self._create_logs_section()
        
        self._load_scripts()
        self._register_hotkey()
    
    def _create_menu(self):
        menubar = tk.Menu(self)
        self.configure(menu=menubar)
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=Lang.t("settings"), menu=settings_menu)
        
        language_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label=Lang.t("language"), menu=language_menu)
        
        language_menu.add_command(label=Lang.t("portuguese"), command=lambda: self._change_language("pt"))
        language_menu.add_command(label=Lang.t("english"), command=lambda: self._change_language("en"))
    
    def _change_language(self, lang):
        if lang != Lang.get():
            Lang.set(lang)
            _save_language(lang)
            messagebox.showinfo(Lang.t("settings"), Lang.t("language_changed"))
    
    def _create_header(self):
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(header_frame, text=Lang.t("application"), font=("Arial", 14)).grid(row=0, column=0, padx=(10, 5), pady=15)
        
        self.app_combo = ctk.CTkComboBox(header_frame, values=[], width=400, font=("Arial", 12))
        self.app_combo.grid(row=0, column=1, padx=(5, 10), pady=15, sticky="ew")
        
        self.refresh_btn = ctk.CTkButton(header_frame, text="⟳", width=40, command=self._refresh_apps)
        self.refresh_btn.grid(row=0, column=2, padx=(0, 10), pady=15)
        
        self.logs_switch_var = ctk.BooleanVar(value=False)
        self.logs_switch = ctk.CTkSwitch(
            header_frame, 
            text=Lang.t("enable_logs"), 
            variable=self.logs_switch_var,
            command=self._toggle_logs
        )
        self.logs_switch.grid(row=0, column=3, padx=(10, 10), pady=15)
        
        self._refresh_apps()
    
    def _create_profile_section(self):
        profile_frame = ctk.CTkFrame(self)
        profile_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(profile_frame, text=Lang.t("profile"), font=("Arial", 14)).pack(side="left", padx=(10, 5), pady=10)
        
        self.profile_combo = ctk.CTkComboBox(
            profile_frame, 
            values=self._get_profiles(),
            width=200,
            font=("Arial", 12),
            command=self._on_profile_change
        )
        self.profile_combo.set(self.current_profile)
        self.profile_combo.pack(side="left", padx=(0, 10), pady=10)
        
        self.new_profile_entry = ctk.CTkEntry(
            profile_frame,
            placeholder_text=Lang.t("new_profile_placeholder"),
            width=150,
            font=("Arial", 12)
        )
        self.new_profile_entry.pack(side="left", padx=(0, 5), pady=10)
        
        ctk.CTkButton(
            profile_frame,
            text="+",
            width=40,
            command=self._create_profile
        ).pack(side="left", padx=(0, 10), pady=10)
        
        ctk.CTkButton(
            profile_frame,
            text="✎",
            width=40,
            fg_color="#E67E22",
            hover_color="#D35400",
            command=self._rename_profile
        ).pack(side="left", padx=(0, 5), pady=10)
        
        ctk.CTkButton(
            profile_frame,
            text="🗑",
            width=40,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=self._delete_profile
        ).pack(side="left", pady=10)
        
        self.toggle_hotkey_btn = ctk.CTkButton(
            profile_frame,
            text=f"{Lang.t('hotkey_toggle')} {self.toggle_hotkey}",
            font=("Arial", 12),
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            width=200,
            command=self._start_toggle_hotkey_capture
        )
        self.toggle_hotkey_btn.pack(side="right", padx=(0, 10), pady=10)
    
    def _get_profiles(self):
        return sorted(self.profiles_list) if self.profiles_list else [DEFAULT_PROFILE]
    
    def _refresh_profiles(self):
        profiles = self._get_profiles()
        self.profile_combo.configure(values=profiles)
    
    def _on_profile_change(self, profile_name):
        if profile_name != self.current_profile:
            self.current_profile = profile_name
            self._save_profiles_config()
            self._load_scripts()
    
    def _create_profile(self):
        name = self.new_profile_entry.get().strip()
        if not name:
            messagebox.showwarning(Lang.t("warning"), Lang.t("profile_name_required"))
            return
        
        name = name.replace(".json", "").replace(" ", "_")
        
        if name in self.profiles_list:
            messagebox.showwarning(Lang.t("warning"), Lang.t("profile_exists"))
            return
        
        new_file = os.path.join(PROFILES_DIR, f"{name}.json")
        current_file = self._get_config_file()
        
        if os.path.exists(current_file):
            with open(current_file, "r", encoding="utf-8") as f:
                data = f.read()
            with open(new_file, "w", encoding="utf-8") as f:
                f.write(data)
        else:
            with open(new_file, "w", encoding="utf-8") as f:
                json.dump({"scripts": [], "global_vars": ""}, f, indent=2)
        
        self.profiles_list.append(name)
        self.current_profile = name
        self._save_profiles_config()
        
        self.new_profile_entry.delete(0, "end")
        self._refresh_profiles()
        self.profile_combo.set(name)
        self._load_scripts()
        messagebox.showinfo(Lang.t("success"), Lang.t("profile_created").format(name=name))
    
    def _rename_profile(self):
        if self.current_profile == DEFAULT_PROFILE:
            messagebox.showwarning(Lang.t("warning"), Lang.t("cannot_rename_default"))
            return
        
        new_name = self.new_profile_entry.get().strip()
        if not new_name:
            messagebox.showwarning(Lang.t("warning"), Lang.t("new_name_required"))
            return
        
        new_name = new_name.replace(".json", "").replace(" ", "_")
        
        if new_name in self.profiles_list:
            messagebox.showwarning(Lang.t("warning"), Lang.t("profile_exists"))
            return
        
        old_file = os.path.join(PROFILES_DIR, f"{self.current_profile}.json")
        new_file = os.path.join(PROFILES_DIR, f"{new_name}.json")
        
        if os.path.exists(old_file):
            os.rename(old_file, new_file)
        
        idx = self.profiles_list.index(self.current_profile)
        self.profiles_list[idx] = new_name
        self.current_profile = new_name
        self._save_profiles_config()
        
        self.new_profile_entry.delete(0, "end")
        self._refresh_profiles()
        self.profile_combo.set(new_name)
        messagebox.showinfo(Lang.t("success"), Lang.t("profile_renamed").format(name=new_name))
    
    def _delete_profile(self):
        if self.current_profile == DEFAULT_PROFILE:
            messagebox.showwarning(Lang.t("warning"), Lang.t("cannot_delete_default"))
            return
        
        if not messagebox.askyesno(Lang.t("confirm"), Lang.t("confirm_delete_profile").format(name=self.current_profile)):
            return
        
        file_path = os.path.join(PROFILES_DIR, f"{self.current_profile}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
        
        self.profiles_list.remove(self.current_profile)
        self.current_profile = DEFAULT_PROFILE
        self._save_profiles_config()
        
        self._refresh_profiles()
        self.profile_combo.set(DEFAULT_PROFILE)
        self._load_scripts()
        messagebox.showinfo(Lang.t("success"), Lang.t("profile_deleted"))
    
    def _create_picker_section(self):
        picker_frame = ctk.CTkFrame(self)
        picker_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(picker_frame, text=Lang.t("screen_capture"), font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        controls_frame = ctk.CTkFrame(picker_frame, fg_color="transparent")
        controls_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.coords_btn = ctk.CTkButton(
            controls_frame,
            text=f"{Lang.t('coordinates')} --",
            font=("Arial", 12),
            fg_color="#3B3B3B",
            hover_color="#4A4A4A",
            width=180,
            command=self._copy_coords
        )
        self.coords_btn.pack(side="left", padx=(0, 10))
        
        color_container = ctk.CTkFrame(controls_frame, fg_color="transparent")
        color_container.pack(side="left", padx=(0, 10))
        
        self.color_btn = ctk.CTkButton(
            color_container,
            text=f"{Lang.t('color')} --",
            font=("Arial", 12),
            fg_color="#3B3B3B",
            hover_color="#4A4A4A",
            width=140,
            command=self._copy_color
        )
        self.color_btn.pack(side="left")
        
        self.color_preview = ctk.CTkFrame(
            color_container,
            width=30,
            height=30,
            fg_color="#2B2B2B",
            border_width=2,
            border_color="#555555"
        )
        self.color_preview.pack(side="left", padx=(5, 0))
        self.color_preview.pack_propagate(False)
        
        self.hotkey_btn = ctk.CTkButton(
            controls_frame,
            text=f"{Lang.t('hotkey')} {self.current_hotkey}",
            font=("Arial", 12),
            fg_color="#5D5D5D",
            hover_color="#6D6D6D",
            width=150,
            command=self._start_hotkey_capture
        )
        self.hotkey_btn.pack(side="left")
        
        area_frame = ctk.CTkFrame(picker_frame, fg_color="transparent")
        area_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        ctk.CTkLabel(area_frame, text=Lang.t("area_capture_ocr"), font=("Arial", 12, "bold")).pack(side="left", padx=(0, 10))
        
        self.area_btn = ctk.CTkButton(
            area_frame,
            text=f"{Lang.t('area')} --",
            font=("Arial", 12),
            fg_color="#3B3B3B",
            hover_color="#4A4A4A",
            width=280,
            command=self._copy_area
        )
        self.area_btn.pack(side="left", padx=(0, 10))
        
        self.area_capture_btn = ctk.CTkButton(
            area_frame,
            text=Lang.t("select_area"),
            font=("Arial", 12),
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            width=150,
            command=self._start_area_capture
        )
        self.area_capture_btn.pack(side="left")
    
    def _register_hotkey(self):
        try:
            keyboard.unhook_all_hotkeys()
        except:
            pass
        keyboard.add_hotkey(self.current_hotkey, self._capture_screen_info)
        keyboard.add_hotkey(self.toggle_hotkey, self._toggle_execution)
    
    def _start_toggle_hotkey_capture(self):
        if self.waiting_for_toggle_hotkey:
            return
        
        self.waiting_for_toggle_hotkey = True
        self.toggle_hotkey_btn.configure(text=Lang.t("press_key"), fg_color="#E67E22")
        
        def on_key_event(event):
            if not self.waiting_for_toggle_hotkey:
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
                    self.toggle_hotkey = "+".join(modifiers) + "+" + key
                else:
                    self.toggle_hotkey = key
                
                self.waiting_for_toggle_hotkey = False
                self.toggle_hotkey_btn.configure(
                    text=f"{Lang.t('hotkey_toggle')} {self.toggle_hotkey}",
                    fg_color="#9B59B6"
                )
                keyboard.unhook(hook)
                self._save_profiles_config()
                self._register_hotkey()
        
        hook = keyboard.on_press(on_key_event)
    
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
                    self.current_hotkey = "+".join(modifiers) + "+" + key
                else:
                    self.current_hotkey = key
                
                self.waiting_for_hotkey = False
                self.hotkey_btn.configure(
                    text=f"{Lang.t('hotkey')} {self.current_hotkey}",
                    fg_color="#5D5D5D"
                )
                keyboard.unhook(hook)
                self._register_hotkey()
        
        hook = keyboard.on_press(on_key_event)
    
    def _capture_screen_info(self):
        x, y = pyautogui.position()
        self.captured_coords = (x, y)
        
        try:
            screenshot = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))
            pixel = screenshot.getpixel((0, 0))
            self.captured_color = "#{:02X}{:02X}{:02X}".format(pixel[0], pixel[1], pixel[2])
        except Exception as e:
            print(f"Erro ao capturar cor: {e}")
            self.captured_color = "#000000"
        
        self.after(0, self._update_picker_ui)
    
    def _update_picker_ui(self):
        if self.captured_coords:
            self.coords_btn.configure(text=f"{Lang.t('coordinates')} {self.captured_coords[0]}, {self.captured_coords[1]}")
        
        if self.captured_color:
            self.color_btn.configure(text=f"{Lang.t('color')} {self.captured_color}")
            self.color_preview.configure(fg_color=self.captured_color)
    
    def _copy_coords(self):
        if self.captured_coords:
            text = f"{self.captured_coords[0]}, {self.captured_coords[1]}"
            self.clipboard_clear()
            self.clipboard_append(text)
            self.coords_btn.configure(text=Lang.t("copied"), fg_color="#27AE60")
            self.after(1000, lambda: self.coords_btn.configure(
                text=f"{Lang.t('coordinates')} {self.captured_coords[0]}, {self.captured_coords[1]}",
                fg_color="#3B3B3B"
            ))
    
    def _copy_color(self):
        if self.captured_color:
            self.clipboard_clear()
            self.clipboard_append(self.captured_color)
            self.color_btn.configure(text=Lang.t("copied"), fg_color="#27AE60")
            self.after(1000, lambda: self.color_btn.configure(
                text=f"{Lang.t('color')} {self.captured_color}",
                fg_color="#3B3B3B"
            ))
    
    def _start_area_capture(self):
        self.withdraw()
        self.after(100, self._open_area_selector)
    
    def _open_area_selector(self):
        AreaSelector(self._on_area_selected)
    
    def _on_area_selected(self, x1, y1, x2, y2):
        self.deiconify()
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))
        
        if x1 is not None:
            self.captured_area_start = (x1, y1)
            self.captured_area_end = (x2, y2)
            self.area_btn.configure(
                text=f"{Lang.t('area')} {x1}, {y1}, {x2}, {y2}"
            )
    
    def _copy_area(self):
        if self.captured_area_start and self.captured_area_end:
            x1, y1 = self.captured_area_start
            x2, y2 = self.captured_area_end
            text = f"{x1}, {y1}, {x2}, {y2}"
            self.clipboard_clear()
            self.clipboard_append(text)
            self.area_btn.configure(text=Lang.t("copied"), fg_color="#27AE60")
            self.after(1000, lambda: self.area_btn.configure(
                text=f"{Lang.t('area')} {x1}, {y1}, {x2}, {y2}",
                fg_color="#3B3B3B"
            ))
    
    def _create_add_button(self):
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        btn_frame.grid_columnconfigure(1, weight=1)
        
        self.add_btn = ctk.CTkButton(btn_frame, text=Lang.t("add_script"), font=("Arial", 14), command=self._open_add_modal)
        self.add_btn.pack(side="left")
        
        self.global_vars_btn = ctk.CTkButton(
            btn_frame, 
            text=Lang.t("global_vars"), 
            font=("Arial", 14),
            fg_color="#9B59B6",
            hover_color="#8E44AD",
            command=self._open_global_vars_modal
        )
        self.global_vars_btn.pack(side="left", padx=(10, 0))
        
        self.start_btn = ctk.CTkButton(
            btn_frame, 
            text=Lang.t("start"), 
            font=("Arial", 14, "bold"),
            fg_color="#27AE60",
            hover_color="#1E8449",
            width=150,
            command=self._toggle_execution
        )
        self.start_btn.pack(side="right")
    
    def _create_scripts_list(self):
        self.list_frame = ctk.CTkScrollableFrame(self, label_text=Lang.t("scripts"))
        self.list_frame.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)
    
    def _create_logs_section(self):
        self.logs_container = ctk.CTkFrame(self)
        self.logs_container.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.logs_container.grid_remove()
        
        header = ctk.CTkFrame(self.logs_container, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(header, text=Lang.t("logs"), font=("Arial", 14, "bold")).pack(side="left")
        
        ctk.CTkButton(
            header, 
            text=Lang.t("clear"), 
            width=70, 
            height=24,
            command=self._clear_logs
        ).pack(side="right", padx=(5, 0))
        
        ctk.CTkButton(
            header, 
            text=Lang.t("clear_color_cache"), 
            width=150, 
            height=24,
            fg_color="#E67E22",
            hover_color="#D35400",
            command=self._clear_color_cache
        ).pack(side="right")
        
        self.logs_frame = ctk.CTkScrollableFrame(self.logs_container, height=150)
        self.logs_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        LogManager.set_log_frame(self.logs_frame)
    
    def _toggle_logs(self):
        self.logs_enabled = self.logs_switch_var.get()
        LogManager.set_enabled(self.logs_enabled)
        
        if self.logs_enabled:
            self.logs_container.grid()
            self.grid_rowconfigure(4, weight=0)
        else:
            self.logs_container.grid_remove()
    
    def _clear_logs(self):
        for widget in self.logs_frame.winfo_children():
            widget.destroy()
    
    def _clear_color_cache(self):
        Debugger._seen_colors.clear()
    
    def _refresh_apps(self):
        apps = self._get_running_apps()
        self.app_combo.configure(values=apps)
        if apps:
            self.app_combo.set(apps[0])
    
    def _get_running_apps(self):
        windows = []
        
        def enum_windows_callback(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    try:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        proc = psutil.Process(pid)
                        app_name = f"{title} ({proc.name()})"
                        if app_name not in results:
                            results.append(app_name)
                    except:
                        pass
            return True
        
        win32gui.EnumWindows(enum_windows_callback, windows)
        return sorted(windows)
    
    def _open_add_modal(self):
        ScriptModal(self, self._on_script_saved)
    
    def _open_edit_modal(self, script_data):
        ScriptModal(self, self._on_script_saved, script_data)
    
    def _open_global_vars_modal(self):
        GlobalVarsModal(self, self._on_global_vars_saved, self.global_vars_code)
    
    def _on_global_vars_saved(self, code):
        self.global_vars_code = code
        self._save_scripts()
    
    def _on_script_saved(self, new_data, old_data=None):
        if old_data:
            idx = self.scripts.index(old_data)
            self.scripts[idx] = new_data
        else:
            self.scripts.append(new_data)
        
        self._save_scripts()
        self._refresh_list()
    
    def _on_script_toggle(self, script_data):
        self._save_scripts()
    
    def _on_script_delete(self, script_data):
        if messagebox.askyesno(Lang.t("confirm"), Lang.t("confirm_delete_script").format(name=script_data['title'])):
            self.scripts.remove(script_data)
            self._save_scripts()
            self._refresh_list()
    
    def _refresh_list(self):
        for widget in self.script_widgets:
            widget.destroy()
        self.script_widgets.clear()
        
        for script in self.scripts:
            item = ScriptItem(
                self.list_frame,
                script,
                self._on_script_toggle,
                self._open_edit_modal,
                self._on_script_delete
            )
            item.pack(fill="x", padx=5, pady=5)
            self.script_widgets.append(item)
    
    def _ensure_config_dir(self):
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        if not os.path.exists(PROFILES_DIR):
            os.makedirs(PROFILES_DIR)
    
    def _load_profiles_config(self):
        if os.path.exists(PROFILES_FILE):
            try:
                with open(PROFILES_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.current_profile = data.get("activeProfile", DEFAULT_PROFILE)
                    self.profiles_list = data.get("profiles", [DEFAULT_PROFILE])
                    self.toggle_hotkey = data.get("toggleHotkey", "f6")
            except Exception as e:
                print(f"Erro ao carregar profiles.json: {e}")
                self.current_profile = DEFAULT_PROFILE
                self.profiles_list = [DEFAULT_PROFILE]
                self.toggle_hotkey = "f6"
        else:
            self.current_profile = DEFAULT_PROFILE
            self.profiles_list = [DEFAULT_PROFILE]
            self.toggle_hotkey = "f6"
            self._save_profiles_config()
        
        if self.current_profile not in self.profiles_list:
            self.profiles_list.append(self.current_profile)
            self._save_profiles_config()
    
    def _save_profiles_config(self):
        try:
            with open(PROFILES_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "activeProfile": self.current_profile,
                    "profiles": self.profiles_list,
                    "toggleHotkey": self.toggle_hotkey
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar profiles.json: {e}")
    
    def _get_config_file(self):
        return os.path.join(PROFILES_DIR, f"{self.current_profile}.json")
    
    def _load_scripts(self):
        config_file = self._get_config_file()
        if os.path.exists(config_file):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.scripts = data.get("scripts", [])
                    self.global_vars_code = data.get("global_vars", "")
            except Exception as e:
                print(f"Erro ao carregar scripts: {e}")
                self.scripts = []
                self.global_vars_code = ""
        else:
            self.scripts = []
            self.global_vars_code = ""
            self._save_scripts()
        
        self._refresh_list()
    
    def _save_scripts(self):
        config_file = self._get_config_file()
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump({
                    "scripts": self.scripts,
                    "global_vars": self.global_vars_code
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar scripts: {e}")
            messagebox.showerror(Lang.t("error"), f"{Lang.t('save_error')} {e}")
    
    def _toggle_execution(self):
        if self.is_running:
            self._stop_scripts()
        else:
            self._start_scripts()
    
    def _start_scripts(self):
        enabled_scripts = [s for s in self.scripts if s.get("enabled", False)]
        
        if not enabled_scripts:
            messagebox.showwarning(Lang.t("warning"), Lang.t("no_active_script"))
            return
        
        selected = self.app_combo.get()
        if selected:
            self.selected_app_title = selected.split(" (")[0] if " (" in selected else selected
        else:
            self.selected_app_title = None
        
        self.is_running = True
        self.attributes('-topmost', True)
        
        self.start_btn.configure(
            text=Lang.t("stop"),
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        
        self._disable_controls(True)
        
        self.script_hotkeys = []
        self.script_stop_events = []
        self.script_executing = {}
        
        for script in enabled_scripts:
            script_id = id(script)
            self.script_executing[script_id] = False
            stop_event = threading.Event()
            self.script_stop_events.append(stop_event)
            
            if script.get("trigger_hotkey"):
                hotkey = keyboard.add_hotkey(
                    script["trigger_hotkey"],
                    lambda s=script, sid=script_id: self._execute_script_once(s, sid)
                )
                self.script_hotkeys.append(hotkey)
            else:
                thread = threading.Thread(
                    target=self._run_script_loop,
                    args=(script, script_id, stop_event),
                    daemon=True
                )
                self.script_threads.append(thread)
                thread.start()
    
    def _stop_scripts(self):
        self.is_running = False
        
        self._kill_pending_scripts()
        
        self.script_threads.clear()
        self.attributes('-topmost', False)
        
        for hotkey in getattr(self, 'script_hotkeys', []):
            try:
                keyboard.remove_hotkey(hotkey)
            except:
                pass
        self.script_hotkeys = []
    
    def _kill_pending_scripts(self):
        for event in self.script_stop_events:
            event.set()
        self.script_stop_events.clear()
        self.script_executing.clear()
        
        self.start_btn.configure(
            text=Lang.t("start"),
            fg_color="#27AE60",
            hover_color="#1E8449"
        )
        
        self._disable_controls(False)
    
    def _disable_controls(self, disabled):
        state = "disabled" if disabled else "normal"
        self.add_btn.configure(state=state)
        self.global_vars_btn.configure(state=state)
        self.app_combo.configure(state=state)
        self.refresh_btn.configure(state=state)
        
        for widget in self.script_widgets:
            widget.switch.configure(state=state)
            widget.edit_btn.configure(state=state)
            widget.delete_btn.configure(state=state)
    
    def _execute_script_once(self, script, script_id=None):
        if not self.is_running:
            return
        
        if script_id is not None and self.script_executing.get(script_id, False):
            return
        
        if script_id is not None:
            self.script_executing[script_id] = True
        
        code = script.get("code", "")
        title = script.get("title", "Sem título")
        
        selected_app = self.selected_app_title
        global_vars = self.global_vars_code
        
        exec_globals = {
            "__builtins__": __builtins__,
            "pyautogui": pyautogui,
            "time": time,
            "os": os,
            "Screen": Screen,
            "Keyboard": Keyboard,
            "Mouse": Mouse,
            "Debugger": Debugger,
            "Sound": Sound,
        }
        
        if global_vars:
            try:
                exec(global_vars, exec_globals)
            except Exception as e:
                print(f"Erro nas variáveis globais: {e}")
        
        try:
            if selected_app:
                focus_window_by_title(selected_app)
                time.sleep(0.1)
            
            exec(code, exec_globals)
        except Exception as e:
            print(f"Erro no script '{title}': {e}")
        finally:
            if script_id is not None:
                self.script_executing[script_id] = False
    
    def _run_script_loop(self, script, script_id, stop_event):
        interval_sec = script.get("interval_ms", 1000) / 1000.0
        code = script.get("code", "")
        title = script.get("title", "Sem título")
        
        selected_app = self.selected_app_title
        global_vars = self.global_vars_code
        
        exec_globals = {
            "__builtins__": __builtins__,
            "pyautogui": pyautogui,
            "time": time,
            "os": os,
            "Screen": Screen,
            "Keyboard": Keyboard,
            "Mouse": Mouse,
            "Debugger": Debugger,
            "Sound": Sound,
        }
        
        if global_vars:
            try:
                exec(global_vars, exec_globals)
            except Exception as e:
                print(f"Erro nas variáveis globais: {e}")
        
        while self.is_running and not stop_event.is_set():
            self.script_executing[script_id] = True
            start_time = time.time()
            
            try:
                if selected_app:
                    focus_window_by_title(selected_app)
                    time.sleep(0.1)
                
                exec(code, exec_globals)
            except Exception as e:
                print(f"Erro no script '{title}': {e}")
            finally:
                self.script_executing[script_id] = False
            
            if not self.is_running or stop_event.is_set():
                break
            
            execution_time = time.time() - start_time
            remaining_time = interval_sec - execution_time
            
            if remaining_time > 0:
                elapsed = 0
                while elapsed < remaining_time and self.is_running and not stop_event.is_set():
                    time.sleep(min(0.1, remaining_time - elapsed))
                    elapsed += 0.1


if __name__ == "__main__":
    app = WardMacroApp()
    app.mainloop()
