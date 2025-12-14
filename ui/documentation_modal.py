import customtkinter as ctk

Lang = None

def init_lang(lang_class):
    global Lang
    Lang = lang_class


class DocumentationModal(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title(Lang.t("docs_title"))
        self.geometry("800x700")
        self.resizable(True, True)
        
        self.transient(parent)
        self.attributes('-topmost', True)
        self.after(100, lambda: self.attributes('-topmost', False))
        self.focus_force()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="ew")
        self.search_frame.grid_remove()
        
        ctk.CTkLabel(self.search_frame, text=Lang.t("search"), font=("Arial", 12)).pack(side="left", padx=(0, 5))
        
        self.search_entry = ctk.CTkEntry(self.search_frame, width=300, font=("Arial", 12))
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self._search_next())
        self.search_entry.bind("<Escape>", lambda e: self._close_search())
        
        ctk.CTkButton(self.search_frame, text=Lang.t("next"), width=80, command=self._search_next).pack(side="left", padx=(0, 5))
        ctk.CTkButton(self.search_frame, text=Lang.t("previous"), width=80, command=self._search_prev).pack(side="left", padx=(0, 5))
        
        self.search_label = ctk.CTkLabel(self.search_frame, text="", font=("Arial", 11))
        self.search_label.pack(side="left", padx=(10, 0))
        
        ctk.CTkButton(self.search_frame, text="✕", width=30, command=self._close_search).pack(side="right")
        
        self.textbox = ctk.CTkTextbox(self, font=("Consolas", 12), wrap="word")
        self.textbox.grid(row=1, column=0, padx=20, pady=(5, 10), sticky="nsew")
        
        docs = self._get_documentation()
        self.textbox.insert("1.0", docs)
        self.textbox.configure(state="disabled")
        
        self.search_matches = []
        self.current_match_idx = -1
        self.last_search_query = ""
        
        self.bind("<Control-f>", self._open_search)
        self.textbox.bind("<Control-f>", self._open_search)
        
        ctk.CTkButton(self, text=Lang.t("close"), command=self.destroy).grid(row=2, column=0, pady=(0, 20))
    
    def _open_search(self, event=None):
        self.search_frame.grid()
        self.search_entry.focus_set()
        self.search_entry.select_range(0, "end")
        return "break"
    
    def _close_search(self):
        self.search_frame.grid_remove()
        self._clear_highlights()
        self.search_entry.delete(0, "end")
        self.search_matches = []
        self.current_match_idx = -1
        self.search_label.configure(text="")
    
    def _clear_highlights(self):
        self.textbox.configure(state="normal")
        self.textbox.tag_remove("highlight", "1.0", "end")
        self.textbox.tag_remove("current_highlight", "1.0", "end")
        self.textbox.configure(state="disabled")
    
    def _search_text(self):
        self._clear_highlights()
        self.search_matches = []
        self.current_match_idx = -1
        
        query = self.search_entry.get().strip().lower()
        self.last_search_query = query
        
        if not query:
            self.search_label.configure(text="")
            return
        
        self.textbox.configure(state="normal")
        self.textbox.tag_config("highlight", background="#4A4A00")
        self.textbox.tag_config("current_highlight", background="#FFD700", foreground="black")
        
        content = self.textbox.get("1.0", "end-1c").lower()
        start_idx = 0
        
        while True:
            pos = content.find(query, start_idx)
            if pos == -1:
                break
            
            line = content[:pos].count('\n') + 1
            col = pos - content.rfind('\n', 0, pos) - 1
            start = f"{line}.{col}"
            end = f"{line}.{col + len(query)}"
            
            self.textbox.tag_add("highlight", start, end)
            self.search_matches.append((start, end))
            start_idx = pos + 1
        
        self.textbox.configure(state="disabled")
        
        if self.search_matches:
            self.current_match_idx = 0
            self._highlight_current()
            self.search_label.configure(text=f"1 / {len(self.search_matches)}")
        else:
            self.search_label.configure(text=Lang.t("not_found"))
    
    def _highlight_current(self):
        if not self.search_matches or self.current_match_idx < 0:
            return
        
        self.textbox.configure(state="normal")
        self.textbox.tag_remove("current_highlight", "1.0", "end")
        
        start, end = self.search_matches[self.current_match_idx]
        self.textbox.tag_add("current_highlight", start, end)
        self.textbox.see(start)
        self.textbox.configure(state="disabled")
    
    def _check_query_changed(self):
        current_query = self.search_entry.get().strip().lower()
        return current_query != self.last_search_query
    
    def _search_next(self):
        query = self.search_entry.get().strip()
        if not query:
            return
        
        if self._check_query_changed() or not self.search_matches:
            self._search_text()
            return
        
        self.current_match_idx = (self.current_match_idx + 1) % len(self.search_matches)
        self._highlight_current()
        self.search_label.configure(text=f"{self.current_match_idx + 1} / {len(self.search_matches)}")
    
    def _search_prev(self):
        query = self.search_entry.get().strip()
        if not query:
            return
        
        if self._check_query_changed() or not self.search_matches:
            self._search_text()
            return
        
        self.current_match_idx = (self.current_match_idx - 1) % len(self.search_matches)
        self._highlight_current()
        self.search_label.configure(text=f"{self.current_match_idx + 1} / {len(self.search_matches)}")
    
    def _get_documentation(self):
        if Lang.get() == "en":
            return self._get_documentation_en()
        return self._get_documentation_pt()
    
    def _get_documentation_pt(self):
        return '''===========================================
       WARD MACRO - DOCUMENTAÇÃO DOS HELPERS
===========================================

═══════════════════════════════════════════
💻 CLASSE: Screen
═══════════════════════════════════════════
Métodos para verificar cores e textos na tela.

⚠️ NOTA: Funções de OCR (getAreaText, areaHasText, etc.)
   requerem Tesseract OCR instalado.
   Download: https://github.com/UB-Mannheim/tesseract/wiki

● Screen.positionHasColor(x, y, hex_color)
  Verifica se uma posição tem uma cor específica.
  
  Parâmetros:
    - x (int): Coordenada X da tela
    - y (int): Coordenada Y da tela  
    - hex_color (str): Cor em hexadecimal (ex: "#FF0000")
  
  Retorna: bool (True se a cor corresponder)
  
  Exemplo:
    if Screen.positionHasColor(100, 200, "#FF0000"):
        print("Encontrou vermelho!")
        Mouse.leftClick(100, 200)

● Screen.positionHasSomeColor(x, y, colors)
  Verifica se uma posição tem alguma das cores da lista.
  
  Parâmetros:
    - x (int): Coordenada X da tela
    - y (int): Coordenada Y da tela
    - colors (list): Lista de cores em hexadecimal
  
  Retorna: bool (True se alguma cor corresponder)
  
  Exemplo:
    cores_alvo = ["#FF0000", "#00FF00", "#0000FF"]
    if Screen.positionHasSomeColor(150, 300, cores_alvo):
        print("Encontrou uma das cores!")

● Screen.getColorAt(x, y)
  Obtém a cor de uma posição da tela.
  
  Parâmetros:
    - x (int): Coordenada X da tela
    - y (int): Coordenada Y da tela
  
  Retorna: str (cor em hexadecimal, ex: "#FF5733")
  
  Exemplo:
    cor = Screen.getColorAt(500, 400)
    print(f"A cor nessa posição é: {cor}")

● Screen.getAreaText(x1, y1, x2, y2)
  Extrai todo o texto de uma área da tela usando OCR.
  
  ⚠️ REQUER TESSERACT OCR INSTALADO!
  Download: https://github.com/UB-Mannheim/tesseract/wiki
  
  Parâmetros:
    - x1, y1 (int): Coordenadas do canto superior esquerdo
    - x2, y2 (int): Coordenadas do canto inferior direito
  
  Retorna: str (texto extraído da área)
  
  Exemplo:
    texto = Screen.getAreaText(100, 100, 500, 200)
    print(f"Texto encontrado: {texto}")
    
    # Verificar conteúdo específico
    if "erro" in texto.lower():
        Sound.beep(500, 300)

● Screen.areaHasText(x1, y1, x2, y2, text)
  Verifica se uma área da tela contém um texto (OCR).
  
  ⚠️ REQUER TESSERACT OCR INSTALADO!
  Download: https://github.com/UB-Mannheim/tesseract/wiki
  
  Parâmetros:
    - x1, y1 (int): Coordenadas do canto superior esquerdo
    - x2, y2 (int): Coordenadas do canto inferior direito
    - text (str): Texto a ser procurado
  
  Retorna: bool (True se o texto for encontrado)
  
  Exemplo:
    if Screen.areaHasText(100, 100, 500, 200, "Iniciar"):
        Mouse.leftClick(300, 150)

● Screen.areaHasAtLeastOneText(x1, y1, x2, y2, texts)
  Verifica se uma área contém ao menos um dos textos.
  
  ⚠️ REQUER TESSERACT OCR INSTALADO!
  Download: https://github.com/UB-Mannheim/tesseract/wiki
  
  Parâmetros:
    - x1, y1 (int): Coordenadas do canto superior esquerdo
    - x2, y2 (int): Coordenadas do canto inferior direito
    - texts (list): Lista de textos a procurar
  
  Retorna: bool (True se ao menos um texto for encontrado)
  
  Exemplo:
    textos = ["OK", "Confirmar", "Aceitar"]
    if Screen.areaHasAtLeastOneText(100, 100, 500, 200, textos):
        Keyboard.sendKey("enter")

● Screen.areaHasAllTexts(x1, y1, x2, y2, texts)
  Verifica se uma área contém todos os textos da lista.
  
  ⚠️ REQUER TESSERACT OCR INSTALADO!
  Download: https://github.com/UB-Mannheim/tesseract/wiki
  
  Parâmetros:
    - x1, y1 (int): Coordenadas do canto superior esquerdo
    - x2, y2 (int): Coordenadas do canto inferior direito
    - texts (list): Lista de textos obrigatórios
  
  Retorna: bool (True se todos os textos forem encontrados)
  
  Exemplo:
    textos = ["Nome", "Email", "Senha"]
    if Screen.areaHasAllTexts(0, 0, 800, 600, textos):
        print("Formulário carregado!")


═══════════════════════════════════════════
⌨️  CLASSE: Keyboard
═══════════════════════════════════════════
Métodos para simular teclado.

● Keyboard.sendKey(key)
  Simula o pressionamento de uma tecla.
  
  Parâmetros:
    - key (str): Nome da tecla
  
  Teclas comuns: "enter", "tab", "space", "backspace", "delete",
                 "escape", "up", "down", "left", "right",
                 "f1" a "f12", "a" a "z", "0" a "9"
  
  Exemplo:
    Keyboard.sendKey("enter")
    Keyboard.sendKey("f5")
    Keyboard.sendKey("a")

● Keyboard.hotkey(*keys)
  Simula uma combinação de teclas.
  
  Parâmetros:
    - *keys: Teclas a serem pressionadas juntas
  
  Exemplo:
    Keyboard.hotkey("ctrl", "c")      # Copiar
    Keyboard.hotkey("ctrl", "v")      # Colar
    Keyboard.hotkey("alt", "tab")     # Alternar janela
    Keyboard.hotkey("ctrl", "shift", "n")  # 3 teclas

● Keyboard.typeText(text, interval=0.0)
  Digita um texto caractere por caractere.
  
  Parâmetros:
    - text (str): Texto a ser digitado
    - interval (float): Intervalo entre cada tecla (segundos)
  
  Exemplo:
    Keyboard.typeText("Hello World")
    Keyboard.typeText("texto lento", interval=0.1)


═══════════════════════════════════════════
🖱️  CLASSE: Mouse
═══════════════════════════════════════════
Métodos para simular mouse.

● Mouse.leftClick(x, y)
  Executa um clique esquerdo na posição.
  
  Exemplo:
    Mouse.leftClick(500, 300)

● Mouse.rightClick(x, y)
  Executa um clique direito na posição.
  
  Exemplo:
    Mouse.rightClick(500, 300)

● Mouse.middleClick(x, y)
  Executa um clique do botão do meio na posição.
  
  Exemplo:
    Mouse.middleClick(500, 300)

● Mouse.doubleClick(x, y)
  Executa um duplo clique na posição.
  
  Exemplo:
    Mouse.doubleClick(500, 300)

● Mouse.moveTo(x, y)
  Move o cursor para a posição sem clicar.
  
  Exemplo:
    Mouse.moveTo(500, 300)


═══════════════════════════════════════════
🔊 CLASSE: Sound
═══════════════════════════════════════════
Métodos para emitir sons.

● Sound.beep(frequency=1000, duration=200)
  Emite um beep do Windows.
  
  Parâmetros:
    - frequency (int): Frequência em Hz (37 a 32767)
    - duration (int): Duração em milissegundos
  
  Exemplo:
    Sound.beep()                    # Beep padrão
    Sound.beep(2000, 500)           # Tom mais agudo, mais longo
    Sound.beep(frequency=500, duration=100)  # Tom grave, curto


═══════════════════════════════════════════
🔍 CLASSE: Debugger
═══════════════════════════════════════════
Métodos para depuração.

● Debugger.debugColor(x, y)
  Abre uma janela mostrando a cor da posição.
  Também adiciona a cor no painel de logs (se ativado).
  Cores já exibidas não são repetidas.
  
  Exemplo:
    Debugger.debugColor(100, 200)

● Debugger.printText(text, show_alert=False)
  Exibe um texto no painel de logs.
  Se show_alert=True, também exibe um alerta.
  
  Parâmetros:
    - text (str): Texto a ser exibido
    - show_alert (bool): Se True, exibe também um alerta
  
  Exemplo:
    Debugger.printText("Iniciando processo...")
    Debugger.printText("Erro encontrado!", True)


═══════════════════════════════════════════
💡 EXEMPLOS COMPLETOS
═══════════════════════════════════════════

# Exemplo 1: Clicar quando encontrar cor
if Screen.positionHasColor(800, 600, "#00FF00"):
    Mouse.leftClick(800, 600)
    time.sleep(0.5)
    Keyboard.sendKey("enter")

# Exemplo 2: Loop esperando cor aparecer
while not Screen.positionHasColor(100, 100, "#FF0000"):
    time.sleep(0.1)
Mouse.leftClick(100, 100)

# Exemplo 3: Ação baseada em múltiplas cores
if Screen.positionHasSomeColor(200, 200, ["#FF0000", "#00FF00"]):
    Mouse.doubleClick(200, 200)
    Keyboard.hotkey("ctrl", "a")
    Keyboard.hotkey("ctrl", "c")

# Exemplo 4: Automação de formulário
Mouse.leftClick(300, 400)  # Clica no campo
time.sleep(0.2)
Keyboard.typeText("meu texto", interval=0.05)
Keyboard.sendKey("tab")
Keyboard.typeText("outro campo")
Keyboard.sendKey("enter")

# Exemplo 5: Debug para descobrir cor
Debugger.debugColor(500, 500)

═══════════════════════════════════════════
⚠️  DICAS IMPORTANTES
═══════════════════════════════════════════

1. Use time.sleep() entre ações para dar tempo
   da interface responder.

2. As coordenadas são absolutas da tela inteira,
   não relativas à janela da aplicação.

3. Use a hotkey (Ctrl+F12 por padrão) para
   capturar coordenadas e cores facilmente.

4. O módulo "time" já está disponível nos scripts.

5. Cores são case-insensitive (#ff0000 = #FF0000).

6. Para usar funções de OCR (reconhecimento de texto),
   é necessário instalar o Tesseract OCR:
   https://github.com/UB-Mannheim/tesseract/wiki
'''

    def _get_documentation_en(self):
        return '''===========================================
       WARD MACRO - HELPERS DOCUMENTATION
===========================================

═══════════════════════════════════════════
💻 CLASS: Screen
═══════════════════════════════════════════
Methods to check colors and text on screen.

⚠️ NOTE: OCR functions (getAreaText, areaHasText, etc.)
   require Tesseract OCR installed.
   Download: https://github.com/UB-Mannheim/tesseract/wiki

● Screen.positionHasColor(x, y, hex_color)
  Checks if a position has a specific color.
  
  Parameters:
    - x (int): Screen X coordinate
    - y (int): Screen Y coordinate  
    - hex_color (str): Color in hexadecimal (e.g.: "#FF0000")
  
  Returns: bool (True if color matches)
  
  Example:
    if Screen.positionHasColor(100, 200, "#FF0000"):
        print("Found red!")
        Mouse.leftClick(100, 200)

● Screen.positionHasSomeColor(x, y, colors)
  Checks if a position has any color from the list.
  
  Parameters:
    - x (int): Screen X coordinate
    - y (int): Screen Y coordinate
    - colors (list): List of colors in hexadecimal
  
  Returns: bool (True if any color matches)
  
  Example:
    target_colors = ["#FF0000", "#00FF00", "#0000FF"]
    if Screen.positionHasSomeColor(150, 300, target_colors):
        print("Found one of the colors!")

● Screen.getColorAt(x, y)
  Gets the color at a screen position.
  
  Parameters:
    - x (int): Screen X coordinate
    - y (int): Screen Y coordinate
  
  Returns: str (color in hexadecimal, e.g.: "#FF5733")
  
  Example:
    color = Screen.getColorAt(500, 400)
    print(f"The color at this position is: {color}")

● Screen.getAreaText(x1, y1, x2, y2)
  Extracts all text from a screen area using OCR.
  
  ⚠️ REQUIRES TESSERACT OCR INSTALLED!
  Download: https://github.com/UB-Mannheim/tesseract/wiki
  
  Parameters:
    - x1, y1 (int): Top-left corner coordinates
    - x2, y2 (int): Bottom-right corner coordinates
  
  Returns: str (extracted text from area)
  
  Example:
    text = Screen.getAreaText(100, 100, 500, 200)
    print(f"Text found: {text}")
    
    # Check specific content
    if "error" in text.lower():
        Sound.beep(500, 300)

● Screen.areaHasText(x1, y1, x2, y2, text)
  Checks if a screen area contains a text (OCR).
  
  ⚠️ REQUIRES TESSERACT OCR INSTALLED!
  Download: https://github.com/UB-Mannheim/tesseract/wiki
  
  Parameters:
    - x1, y1 (int): Top-left corner coordinates
    - x2, y2 (int): Bottom-right corner coordinates
    - text (str): Text to search for
  
  Returns: bool (True if text is found)
  
  Example:
    if Screen.areaHasText(100, 100, 500, 200, "Start"):
        Mouse.leftClick(300, 150)

● Screen.areaHasAtLeastOneText(x1, y1, x2, y2, texts)
  Checks if an area contains at least one of the texts.
  
  ⚠️ REQUIRES TESSERACT OCR INSTALLED!
  Download: https://github.com/UB-Mannheim/tesseract/wiki
  
  Parameters:
    - x1, y1 (int): Top-left corner coordinates
    - x2, y2 (int): Bottom-right corner coordinates
    - texts (list): List of texts to search
  
  Returns: bool (True if at least one text is found)
  
  Example:
    texts = ["OK", "Confirm", "Accept"]
    if Screen.areaHasAtLeastOneText(100, 100, 500, 200, texts):
        Keyboard.sendKey("enter")

● Screen.areaHasAllTexts(x1, y1, x2, y2, texts)
  Checks if an area contains all texts from the list.
  
  ⚠️ REQUIRES TESSERACT OCR INSTALLED!
  Download: https://github.com/UB-Mannheim/tesseract/wiki
  
  Parameters:
    - x1, y1 (int): Top-left corner coordinates
    - x2, y2 (int): Bottom-right corner coordinates
    - texts (list): List of required texts
  
  Returns: bool (True if all texts are found)
  
  Example:
    texts = ["Name", "Email", "Password"]
    if Screen.areaHasAllTexts(0, 0, 800, 600, texts):
        print("Form loaded!")


═══════════════════════════════════════════
⌨️  CLASS: Keyboard
═══════════════════════════════════════════
Methods to simulate keyboard.

● Keyboard.sendKey(key)
  Simulates a key press.
  
  Parameters:
    - key (str): Key name
  
  Common keys: "enter", "tab", "space", "backspace", "delete",
               "escape", "up", "down", "left", "right",
               "f1" to "f12", "a" to "z", "0" to "9"
  
  Example:
    Keyboard.sendKey("enter")
    Keyboard.sendKey("f5")
    Keyboard.sendKey("a")

● Keyboard.hotkey(*keys)
  Simulates a key combination.
  
  Parameters:
    - *keys: Keys to be pressed together
  
  Example:
    Keyboard.hotkey("ctrl", "c")      # Copy
    Keyboard.hotkey("ctrl", "v")      # Paste
    Keyboard.hotkey("alt", "tab")     # Switch window
    Keyboard.hotkey("ctrl", "shift", "n")  # 3 keys

● Keyboard.typeText(text, interval=0.0)
  Types text character by character.
  
  Parameters:
    - text (str): Text to be typed
    - interval (float): Interval between each key (seconds)
  
  Example:
    Keyboard.typeText("Hello World")
    Keyboard.typeText("slow text", interval=0.1)


═══════════════════════════════════════════
🖱️  CLASS: Mouse
═══════════════════════════════════════════
Methods to simulate mouse.

● Mouse.leftClick(x, y)
  Performs a left click at position.
  
  Example:
    Mouse.leftClick(500, 300)

● Mouse.rightClick(x, y)
  Performs a right click at position.
  
  Example:
    Mouse.rightClick(500, 300)

● Mouse.middleClick(x, y)
  Performs a middle button click at position.
  
  Example:
    Mouse.middleClick(500, 300)

● Mouse.doubleClick(x, y)
  Performs a double click at position.
  
  Example:
    Mouse.doubleClick(500, 300)

● Mouse.moveTo(x, y)
  Moves cursor to position without clicking.
  
  Example:
    Mouse.moveTo(500, 300)


═══════════════════════════════════════════
🔊 CLASS: Sound
═══════════════════════════════════════════
Methods to emit sounds.

● Sound.beep(frequency=1000, duration=200)
  Emits a Windows beep.
  
  Parameters:
    - frequency (int): Frequency in Hz (37 to 32767)
    - duration (int): Duration in milliseconds
  
  Example:
    Sound.beep()                    # Default beep
    Sound.beep(2000, 500)           # Higher pitch, longer
    Sound.beep(frequency=500, duration=100)  # Low pitch, short


═══════════════════════════════════════════
🔍 CLASS: Debugger
═══════════════════════════════════════════
Methods for debugging.

● Debugger.debugColor(x, y)
  Opens a window showing the color at position.
  Also adds color to logs panel (if enabled).
  Already displayed colors are not repeated.
  
  Example:
    Debugger.debugColor(100, 200)

● Debugger.printText(text, show_alert=False)
  Displays text in the logs panel.
  If show_alert=True, also shows an alert.
  
  Parameters:
    - text (str): Text to display
    - show_alert (bool): If True, also shows an alert
  
  Example:
    Debugger.printText("Starting process...")
    Debugger.printText("Error found!", True)


═══════════════════════════════════════════
💡 COMPLETE EXAMPLES
═══════════════════════════════════════════

# Example 1: Click when color is found
if Screen.positionHasColor(800, 600, "#00FF00"):
    Mouse.leftClick(800, 600)
    time.sleep(0.5)
    Keyboard.sendKey("enter")

# Example 2: Loop waiting for color
while not Screen.positionHasColor(100, 100, "#FF0000"):
    time.sleep(0.1)
Mouse.leftClick(100, 100)

# Example 3: Action based on multiple colors
if Screen.positionHasSomeColor(200, 200, ["#FF0000", "#00FF00"]):
    Mouse.doubleClick(200, 200)
    Keyboard.hotkey("ctrl", "a")
    Keyboard.hotkey("ctrl", "c")

# Example 4: Form automation
Mouse.leftClick(300, 400)  # Click on field
time.sleep(0.2)
Keyboard.typeText("my text", interval=0.05)
Keyboard.sendKey("tab")
Keyboard.typeText("another field")
Keyboard.sendKey("enter")

# Example 5: Debug to discover color
Debugger.debugColor(500, 500)

═══════════════════════════════════════════
⚠️  IMPORTANT TIPS
═══════════════════════════════════════════

1. Use time.sleep() between actions to give time
   for the interface to respond.

2. Coordinates are absolute to the entire screen,
   not relative to the application window.

3. Use the hotkey (Ctrl+F12 by default) to
   capture coordinates and colors easily.

4. The "time" module is already available in scripts.

5. Colors are case-insensitive (#ff0000 = #FF0000).

6. To use OCR functions (text recognition),
   you need to install Tesseract OCR:
   https://github.com/UB-Mannheim/tesseract/wiki
'''
