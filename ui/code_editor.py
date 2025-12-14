import tkinter as tk
import customtkinter as ctk
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
import re
import keyword


HELPER_COMPLETIONS = {
    "Screen": {
        "doc": "Métodos para verificar cores e textos na tela",
        "methods": {
            "positionHasColor": {
                "signature": "positionHasColor(x: int, y: int, hex_color: str) -> bool",
                "doc": "Verifica se uma posição tem uma cor específica"
            },
            "positionHasSomeColor": {
                "signature": "positionHasSomeColor(x: int, y: int, colors: list) -> bool",
                "doc": "Verifica se uma posição tem alguma das cores da lista"
            },
            "getColorAt": {
                "signature": "getColorAt(x: int, y: int) -> str",
                "doc": "Obtém a cor de uma posição da tela"
            },
            "getAreaText": {
                "signature": "getAreaText(x1: int, y1: int, x2: int, y2: int) -> str",
                "doc": "Extrai texto de uma área usando OCR"
            },
            "areaHasText": {
                "signature": "areaHasText(x1: int, y1: int, x2: int, y2: int, text: str) -> bool",
                "doc": "Verifica se uma área contém um texto"
            },
            "areaHasAtLeastOneText": {
                "signature": "areaHasAtLeastOneText(x1: int, y1: int, x2: int, y2: int, texts: list) -> bool",
                "doc": "Verifica se uma área contém ao menos um dos textos"
            },
            "areaHasAllTexts": {
                "signature": "areaHasAllTexts(x1: int, y1: int, x2: int, y2: int, texts: list) -> bool",
                "doc": "Verifica se uma área contém todos os textos"
            }
        }
    },
    "Keyboard": {
        "doc": "Métodos para simular teclado",
        "methods": {
            "sendKey": {
                "signature": "sendKey(key: str)",
                "doc": "Simula o pressionamento de uma tecla"
            },
            "hotkey": {
                "signature": "hotkey(*keys)",
                "doc": "Simula uma combinação de teclas"
            },
            "typeText": {
                "signature": "typeText(text: str, interval: float = 0.0)",
                "doc": "Digita um texto caractere por caractere"
            }
        }
    },
    "Mouse": {
        "doc": "Métodos para simular mouse",
        "methods": {
            "leftClick": {
                "signature": "leftClick(x: int, y: int)",
                "doc": "Executa um clique esquerdo"
            },
            "rightClick": {
                "signature": "rightClick(x: int, y: int)",
                "doc": "Executa um clique direito"
            },
            "middleClick": {
                "signature": "middleClick(x: int, y: int)",
                "doc": "Executa um clique do botão do meio"
            },
            "doubleClick": {
                "signature": "doubleClick(x: int, y: int)",
                "doc": "Executa um duplo clique"
            },
            "moveTo": {
                "signature": "moveTo(x: int, y: int)",
                "doc": "Move o cursor para a posição"
            }
        }
    },
    "Sound": {
        "doc": "Métodos para emitir sons",
        "methods": {
            "beep": {
                "signature": "beep(frequency: int = 1000, duration: int = 200)",
                "doc": "Emite um beep do Windows"
            }
        }
    },
    "Debugger": {
        "doc": "Métodos para depuração",
        "methods": {
            "debugColor": {
                "signature": "debugColor(x: int, y: int)",
                "doc": "Abre uma janela mostrando a cor da posição"
            },
            "printText": {
                "signature": "printText(text: str, show_alert: bool = False)",
                "doc": "Exibe um texto no painel de logs"
            }
        }
    },
    "time": {
        "doc": "Módulo de tempo do Python",
        "methods": {
            "sleep": {
                "signature": "sleep(seconds: float)",
                "doc": "Pausa a execução por X segundos"
            }
        }
    },
    "pyautogui": {
        "doc": "Biblioteca de automação",
        "methods": {
            "click": {
                "signature": "click(x=None, y=None, clicks=1, button='left')",
                "doc": "Clica na posição"
            },
            "moveTo": {
                "signature": "moveTo(x, y, duration=0)",
                "doc": "Move o mouse para a posição"
            },
            "press": {
                "signature": "press(key)",
                "doc": "Pressiona uma tecla"
            },
            "write": {
                "signature": "write(text, interval=0.0)",
                "doc": "Digita um texto"
            },
            "screenshot": {
                "signature": "screenshot(region=None)",
                "doc": "Captura a tela"
            },
            "position": {
                "signature": "position() -> tuple",
                "doc": "Retorna a posição atual do mouse"
            }
        }
    }
}

PYTHON_BUILTINS = [
    "print", "len", "range", "str", "int", "float", "bool", "list", "dict", "tuple",
    "set", "True", "False", "None", "if", "else", "elif", "for", "while", "def",
    "class", "return", "import", "from", "as", "try", "except", "finally", "with",
    "open", "input", "abs", "all", "any", "enumerate", "filter", "map", "max", "min",
    "sorted", "sum", "zip", "isinstance", "type", "hasattr", "getattr", "setattr"
]


class AutocompletePopup(tk.Toplevel):
    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor
        self.withdraw()
        self.overrideredirect(True)
        
        self.listbox = tk.Listbox(
            self,
            font=("Consolas", 11),
            bg="#1E1E1E",
            fg="#D4D4D4",
            selectbackground="#264F78",
            selectforeground="#FFFFFF",
            borderwidth=1,
            relief="solid",
            highlightthickness=0,
            activestyle="none"
        )
        self.listbox.pack(fill="both", expand=True)
        
        self.doc_label = tk.Label(
            self,
            font=("Consolas", 10),
            bg="#252526",
            fg="#9CDCFE",
            anchor="w",
            padx=5,
            pady=2
        )
        
        self.completions = []
        self.visible = False
        
        self.listbox.bind("<Double-Button-1>", self._on_select)
        self.listbox.bind("<<ListboxSelect>>", self._on_highlight)
    
    def show(self, x, y, completions):
        if not completions:
            self.hide()
            return
        
        self.completions = completions
        self.listbox.delete(0, tk.END)
        
        for item in completions:
            if isinstance(item, dict):
                self.listbox.insert(tk.END, f"  {item['name']}")
            else:
                self.listbox.insert(tk.END, f"  {item}")
        
        self.listbox.selection_set(0)
        
        height = min(len(completions), 8) * 20 + 4
        width = max(len(str(c.get('name', c) if isinstance(c, dict) else c)) for c in completions) * 9 + 30
        width = max(width, 200)
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()
        self.lift()
        self.visible = True
        self._on_highlight(None)
    
    def hide(self):
        self.withdraw()
        self.visible = False
        self.doc_label.pack_forget()
    
    def _on_highlight(self, event):
        selection = self.listbox.curselection()
        if selection and self.completions:
            idx = selection[0]
            item = self.completions[idx]
            if isinstance(item, dict) and 'doc' in item:
                self.doc_label.config(text=item.get('signature', item['doc']))
                self.doc_label.pack(fill="x", side="bottom")
            else:
                self.doc_label.pack_forget()
    
    def _on_select(self, event=None):
        selection = self.listbox.curselection()
        if selection:
            idx = selection[0]
            item = self.completions[idx]
            text = item['name'] if isinstance(item, dict) else item
            self.editor._insert_completion(text)
        self.hide()
    
    def select_next(self):
        current = self.listbox.curselection()
        if current:
            idx = current[0]
            if idx < len(self.completions) - 1:
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(idx + 1)
                self.listbox.see(idx + 1)
                self._on_highlight(None)
    
    def select_prev(self):
        current = self.listbox.curselection()
        if current:
            idx = current[0]
            if idx > 0:
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(idx - 1)
                self.listbox.see(idx - 1)
                self._on_highlight(None)
    
    def confirm_selection(self):
        self._on_select()


class CodeEditor(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', 600)
        height = kwargs.pop('height', 300)
        super().__init__(master, width=width, height=height)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.line_numbers = tk.Text(
            self,
            width=4,
            padx=5,
            pady=5,
            font=("Consolas", 12),
            bg="#1E1E1E",
            fg="#858585",
            borderwidth=0,
            highlightthickness=0,
            state="disabled",
            takefocus=0
        )
        self.line_numbers.grid(row=0, column=0, sticky="ns")
        
        self.text = tk.Text(
            self,
            font=("Consolas", 12),
            bg="#1E1E1E",
            fg="#D4D4D4",
            insertbackground="#FFFFFF",
            selectbackground="#264F78",
            selectforeground="#FFFFFF",
            borderwidth=0,
            highlightthickness=0,
            undo=True,
            autoseparators=True,
            wrap="none",
            padx=5,
            pady=5,
            tabs=("4c",)
        )
        self.text.grid(row=0, column=1, sticky="nsew")
        
        self.scrollbar_y = ctk.CTkScrollbar(self, command=self._on_scroll_y)
        self.scrollbar_y.grid(row=0, column=2, sticky="ns")
        
        self.scrollbar_x = ctk.CTkScrollbar(self, orientation="horizontal", command=self.text.xview)
        self.scrollbar_x.grid(row=1, column=1, sticky="ew")
        
        self.text.configure(yscrollcommand=self._on_text_scroll_y, xscrollcommand=self.scrollbar_x.set)
        
        self.lexer = PythonLexer()
        self._setup_tags()
        
        self.autocomplete_popup = None
        self.current_word_start = None
        
        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<KeyPress>", self._on_key_press)
        self.text.bind("<Tab>", self._on_tab)
        self.text.bind("<Shift-Tab>", self._on_shift_tab)
        self.text.bind("<ISO_Left_Tab>", self._on_shift_tab)
        self.text.bind("<Return>", self._on_return)
        self.text.bind("<BackSpace>", self._on_backspace)
        self.text.bind("<Control-z>", self._undo)
        self.text.bind("<Control-Z>", self._undo)
        self.text.bind("<Control-Shift-z>", self._redo)
        self.text.bind("<Control-Shift-Z>", self._redo)
        self.text.bind("<Control-y>", self._redo)
        self.text.bind("<Control-Y>", self._redo)
        self.text.bind("<Control-space>", self._trigger_autocomplete)
        self.text.bind("<Escape>", self._hide_autocomplete)
        self.text.bind("<FocusOut>", self._on_focus_out)
        self.text.bind("<<Modified>>", self._on_modified)
        self.text.bind("<Configure>", lambda e: self._update_line_numbers())
        
        self.line_numbers.bind("<MouseWheel>", lambda e: "break")
        
        self._update_line_numbers()
    
    def _setup_tags(self):
        self.text.tag_configure("keyword", foreground="#569CD6")
        self.text.tag_configure("keyword_namespace", foreground="#C586C0")
        self.text.tag_configure("builtin", foreground="#4EC9B0")
        self.text.tag_configure("function", foreground="#DCDCAA")
        self.text.tag_configure("class", foreground="#4EC9B0")
        self.text.tag_configure("string", foreground="#CE9178")
        self.text.tag_configure("comment", foreground="#6A9955")
        self.text.tag_configure("number", foreground="#B5CEA8")
        self.text.tag_configure("operator", foreground="#D4D4D4")
        self.text.tag_configure("decorator", foreground="#DCDCAA")
        self.text.tag_configure("self", foreground="#569CD6")
        self.text.tag_configure("helper_class", foreground="#4EC9B0", font=("Consolas", 12, "bold"))
        self.text.tag_configure("helper_method", foreground="#DCDCAA")
    
    def _on_scroll_y(self, *args):
        self.text.yview(*args)
        self.line_numbers.yview(*args)
    
    def _on_text_scroll_y(self, first, last):
        self.scrollbar_y.set(first, last)
        self.line_numbers.yview_moveto(first)
    
    def _update_line_numbers(self):
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        
        content = self.text.get("1.0", tk.END)
        lines = content.count('\n')
        
        line_numbers_text = "\n".join(str(i) for i in range(1, lines + 1))
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.configure(state="disabled")
    
    def _on_modified(self, event=None):
        if self.text.edit_modified():
            self._update_line_numbers()
            self.text.edit_modified(False)
    
    def _on_key_release(self, event):
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Shift_L', 'Shift_R', 
                           'Control_L', 'Control_R', 'Alt_L', 'Alt_R', 'Escape'):
            return
        
        self._highlight()
        self._update_line_numbers()
        
        if event.keysym not in ('Return', 'Tab', 'BackSpace', 'Delete'):
            self._check_autocomplete()
    
    def _on_key_press(self, event):
        if self.autocomplete_popup and self.autocomplete_popup.visible:
            if event.keysym == 'Down':
                self.autocomplete_popup.select_next()
                return "break"
            elif event.keysym == 'Up':
                self.autocomplete_popup.select_prev()
                return "break"
            elif event.keysym == 'Return':
                self.autocomplete_popup.confirm_selection()
                return "break"
            elif event.keysym == 'Escape':
                self.autocomplete_popup.hide()
                return "break"
    
    def _on_tab(self, event):
        if self.autocomplete_popup and self.autocomplete_popup.visible:
            self.autocomplete_popup.confirm_selection()
            return "break"
        
        self.text.insert(tk.INSERT, "    ")
        return "break"
    
    def _on_shift_tab(self, event):
        cursor_pos = self.text.index(tk.INSERT)
        line_num = int(cursor_pos.split('.')[0])
        line_start = f"{line_num}.0"
        line_text = self.text.get(line_start, f"{line_num}.end")
        
        if line_text.startswith("    "):
            self.text.delete(line_start, f"{line_num}.4")
        elif line_text.startswith("\t"):
            self.text.delete(line_start, f"{line_num}.1")
        
        return "break"
    
    def _on_return(self, event):
        if self.autocomplete_popup and self.autocomplete_popup.visible:
            self.autocomplete_popup.confirm_selection()
            return "break"
        
        cursor_pos = self.text.index(tk.INSERT)
        line_num = int(cursor_pos.split('.')[0])
        line_start = f"{line_num}.0"
        line_text = self.text.get(line_start, cursor_pos)
        
        indent = ""
        for char in line_text:
            if char in (' ', '\t'):
                indent += char
            else:
                break
        
        stripped = line_text.strip()
        if stripped.endswith(':'):
            indent += "    "
        
        self.text.insert(tk.INSERT, "\n" + indent)
        self._update_line_numbers()
        return "break"
    
    def _on_backspace(self, event):
        cursor_pos = self.text.index(tk.INSERT)
        line_num, col = map(int, cursor_pos.split('.'))
        
        if col >= 4:
            line_start = f"{line_num}.0"
            before_cursor = self.text.get(line_start, cursor_pos)
            if before_cursor and before_cursor[-4:] == "    " and before_cursor.strip() == "":
                self.text.delete(f"{cursor_pos} - 4 chars", cursor_pos)
                return "break"
        
        return None
    
    def _undo(self, event=None):
        try:
            self.text.edit_undo()
            self._highlight()
            self._update_line_numbers()
        except:
            pass
        return "break"
    
    def _redo(self, event=None):
        try:
            self.text.edit_redo()
            self._highlight()
            self._update_line_numbers()
        except:
            pass
        return "break"
    
    def _highlight(self):
        code = self.text.get("1.0", "end-1c")
        
        for tag in ["keyword", "keyword_namespace", "builtin", "function", "class", 
                    "string", "comment", "number", "operator", "decorator", "self",
                    "helper_class", "helper_method"]:
            self.text.tag_remove(tag, "1.0", "end")
        
        tokens = lex(code, self.lexer)
        line = 1
        col = 0
        
        for token_type, token_value in tokens:
            start = f"{line}.{col}"
            
            for char in token_value:
                if char == '\n':
                    line += 1
                    col = 0
                else:
                    col += 1
            
            end = f"{line}.{col}"
            
            tag = None
            if token_type in Token.Keyword:
                if token_type == Token.Keyword.Namespace:
                    tag = "keyword_namespace"
                else:
                    tag = "keyword"
            elif token_type in Token.Name.Builtin:
                tag = "builtin"
            elif token_type in Token.Name.Function:
                tag = "function"
            elif token_type in Token.Name.Class:
                tag = "class"
            elif token_type in Token.Name.Decorator:
                tag = "decorator"
            elif token_type in Token.String:
                tag = "string"
            elif token_type in Token.Comment:
                tag = "comment"
            elif token_type in Token.Number:
                tag = "number"
            elif token_value == "self":
                tag = "self"
            elif token_value in HELPER_COMPLETIONS:
                tag = "helper_class"
            
            if tag:
                self.text.tag_add(tag, start, end)
    
    def _get_current_word(self):
        cursor_pos = self.text.index(tk.INSERT)
        line_num, col = cursor_pos.split('.')
        line_start = f"{line_num}.0"
        line_text = self.text.get(line_start, cursor_pos)
        
        match = re.search(r'[\w.]+$', line_text)
        if match:
            word = match.group()
            start_col = int(col) - len(word)
            return word, f"{line_num}.{start_col}"
        return "", cursor_pos
    
    def _check_autocomplete(self):
        word, start_pos = self._get_current_word()
        self.current_word_start = start_pos
        
        if not word or len(word) < 1:
            self._hide_autocomplete()
            return
        
        completions = self._get_completions(word)
        
        if completions:
            self._show_autocomplete(completions)
        else:
            self._hide_autocomplete()
    
    def _get_completions(self, word):
        completions = []
        
        if '.' in word:
            parts = word.rsplit('.', 1)
            class_name = parts[0]
            method_prefix = parts[1].lower() if len(parts) > 1 else ""
            
            if class_name in HELPER_COMPLETIONS:
                methods = HELPER_COMPLETIONS[class_name].get("methods", {})
                for method_name, info in methods.items():
                    if method_name.lower().startswith(method_prefix):
                        completions.append({
                            "name": method_name,
                            "signature": info.get("signature", ""),
                            "doc": info.get("doc", "")
                        })
        else:
            word_lower = word.lower()
            
            for class_name, info in HELPER_COMPLETIONS.items():
                if class_name.lower().startswith(word_lower):
                    completions.append({
                        "name": class_name,
                        "signature": "",
                        "doc": info.get("doc", "")
                    })
            
            existing_names = [c['name'] if isinstance(c, dict) else c for c in completions]
            
            for builtin in PYTHON_BUILTINS:
                if builtin.lower().startswith(word_lower) and builtin not in existing_names:
                    completions.append(builtin)
                    existing_names.append(builtin)
            
            for kw in keyword.kwlist:
                if kw.lower().startswith(word_lower) and kw not in existing_names:
                    completions.append(kw)
        
        return completions[:15]
    
    def _show_autocomplete(self, completions):
        if not self.autocomplete_popup:
            self.autocomplete_popup = AutocompletePopup(self.winfo_toplevel(), self)
        
        cursor_pos = self.text.index(tk.INSERT)
        bbox = self.text.bbox(cursor_pos)
        
        if bbox:
            x = self.text.winfo_rootx() + bbox[0]
            y = self.text.winfo_rooty() + bbox[1] + bbox[3] + 2
            self.autocomplete_popup.show(x, y, completions)
    
    def _hide_autocomplete(self, event=None):
        if self.autocomplete_popup:
            self.autocomplete_popup.hide()
    
    def _trigger_autocomplete(self, event=None):
        self._check_autocomplete()
        return "break"
    
    def _on_focus_out(self, event):
        self.after(100, self._check_focus)
    
    def _check_focus(self):
        focused = self.focus_get()
        if self.autocomplete_popup and focused != self.autocomplete_popup.listbox:
            pass
    
    def _insert_completion(self, text):
        word, start_pos = self._get_current_word()
        cursor_pos = self.text.index(tk.INSERT)
        
        if '.' in word:
            parts = word.rsplit('.', 1)
            prefix = parts[1] if len(parts) > 1 else ""
            delete_start = f"{cursor_pos} - {len(prefix)} chars"
            self.text.delete(delete_start, cursor_pos)
        else:
            self.text.delete(start_pos, cursor_pos)
        
        self.text.insert(tk.INSERT, text)
        
        if text in HELPER_COMPLETIONS:
            self.text.insert(tk.INSERT, ".")
            self.after(10, self._check_autocomplete)
        
        self._highlight()
    
    def get(self, start, end):
        return self.text.get(start, end)
    
    def insert(self, index, text):
        self.text.insert(index, text)
        self._highlight()
        self._update_line_numbers()
    
    def delete(self, start, end):
        self.text.delete(start, end)
        self._update_line_numbers()
    
    def set_code(self, code):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", code)
        self._highlight()
        self._update_line_numbers()
    
    def focus_set(self):
        self.text.focus_set()
