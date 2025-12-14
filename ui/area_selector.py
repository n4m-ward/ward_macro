import tkinter as tk

Lang = None

def init_lang(lang_class):
    global Lang
    Lang = lang_class


class AreaSelector(tk.Toplevel):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        
        self.attributes('-fullscreen', True)
        self.attributes('-alpha', 0.3)
        self.attributes('-topmost', True)
        self.configure(bg='black')
        
        self.canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        self.label = tk.Label(
            self, 
            text=Lang.t("drag_to_select"),
            font=("Arial", 16, "bold"),
            fg="white",
            bg="black"
        )
        self.label.place(relx=0.5, y=30, anchor="center")
        
        self.canvas.bind('<ButtonPress-1>', self._on_press)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        self.canvas.bind('<ButtonRelease-1>', self._on_release)
        self.bind('<Escape>', self._on_cancel)
        
        self.focus_force()
    
    def _on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=3, fill='white', stipple='gray50'
        )
    
    def _on_drag(self, event):
        if self.rect_id:
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)
    
    def _on_release(self, event):
        end_x, end_y = event.x, event.y
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        
        self.destroy()
        self.callback(x1, y1, x2, y2)
    
    def _on_cancel(self, event):
        self.destroy()
        self.callback(None, None, None, None)
