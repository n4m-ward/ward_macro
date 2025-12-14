import customtkinter as ctk

Lang = None

def init_lang(lang_class):
    global Lang
    Lang = lang_class


class ScriptItem(ctk.CTkFrame):
    def __init__(self, master, script_data, on_toggle, on_edit, on_delete):
        super().__init__(master)
        self.script_data = script_data
        self.on_toggle = on_toggle
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        self.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self, text=script_data["title"], font=("Arial", 14, "bold"), anchor="w")
        self.title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.interval_label = ctk.CTkLabel(self, text=f"{script_data['interval_ms']}ms", font=("Arial", 12), text_color="gray")
        self.interval_label.grid(row=0, column=1, padx=10, pady=10)
        
        self.switch_var = ctk.BooleanVar(value=script_data.get("enabled", False))
        self.switch = ctk.CTkSwitch(self, text="", variable=self.switch_var, command=self._on_toggle)
        self.switch.grid(row=0, column=2, padx=10, pady=10)
        
        self.edit_btn = ctk.CTkButton(self, text=Lang.t("edit"), width=80, command=self._on_edit)
        self.edit_btn.grid(row=0, column=3, padx=5, pady=10)
        
        self.delete_btn = ctk.CTkButton(self, text=Lang.t("delete"), width=80, fg_color="#E74C3C", hover_color="#C0392B", command=self._on_delete)
        self.delete_btn.grid(row=0, column=4, padx=(5, 10), pady=10)
    
    def _on_toggle(self):
        self.script_data["enabled"] = self.switch_var.get()
        self.on_toggle(self.script_data)
    
    def _on_edit(self):
        self.on_edit(self.script_data)
    
    def _on_delete(self):
        self.on_delete(self.script_data)
