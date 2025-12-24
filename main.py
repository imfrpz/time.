import tkinter as tk
from tkinter import font
from datetime import datetime

class FocusTimer:
    def __init__(self):
        self.root = tk.Tk()
        
        # --- НАСТРОЙКИ ---
        self.minutes = 90
        self.seconds = self.minutes * 60
        self.running = False
        self.is_paused = False 
        
        # ЦВЕТА
        self.colors = {
            "bg": "#000000",       
            "fg": "#FFFFFF",       
            "btn_bg": "#E0E0E0",   
            "btn_text": "#000000", 
            "btn_hover": "#FFFFFF",
            "accent": "#FFD700",   
            "danger": "#FF4444",   
            "selection": "#333333", 
            "caret": "#FFFFFF",
            "meta": "#888888"      
        }

        # --- ОКНО ---
        self.root.overrideredirect(True)      
        self.root.attributes('-topmost', True)
        
        # ВЫСОТА ВСЕГО 70px (Супер компактно)
        self.root.geometry("260x70+100+100") 
        self.root.attributes('-alpha', 0.79)
        self.root.configure(bg=self.colors["bg"])

        # --- ШРИФТЫ ---
        self.font_timer = font.Font(family="Segoe UI", size=38, weight="normal")
        self.font_meta = font.Font(family="Segoe UI", size=8, weight="bold")

        # --- КОМПОНОВКА (Layout) ---
        
        # 1. ЛЕВЫЙ БЛОК (Только Цифры)
        self.left_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(20, 0))

        # ТАЙМЕР
        vcmd = (self.root.register(self.validate_input), '%P')
        self.time_entry = tk.Entry(
            self.left_frame, 
            font=self.font_timer, 
            bg=self.colors["bg"], 
            fg=self.colors["fg"],
            insertbackground=self.colors["caret"], 
            insertwidth=1,
            bd=0, justify='left', width=5,
            validate='key', validatecommand=vcmd,
            readonlybackground=self.colors["bg"], 
            disabledbackground=self.colors["bg"],
            selectbackground=self.colors["selection"],
            selectforeground=self.colors["fg"],
            exportselection=False 
        )
        # Центрируем цифры по вертикали в левой части
        self.time_entry.pack(side="left", anchor="center")

        # 2. ПРАВЫЙ БЛОК (Кнопки + Инфо)
        self.right_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.right_frame.pack(side="right", fill="y", padx=(0, 15))
        
        # Внутри правого блока создаем контейнер, чтобы центрировать его по вертикали
        self.controls_container = tk.Frame(self.right_frame, bg=self.colors["bg"])
        self.controls_container.pack(side="left", anchor="center")

        # ЭТАЖ 1: КНОПКИ
        self.btn_row = tk.Frame(self.controls_container, bg=self.colors["bg"])
        self.btn_row.pack(side="top", anchor="e", pady=(0, 2)) # anchor="e" (East) прижимает вправо

        self.btn_start = self.create_btn(self.btn_row, "▶", self.toggle)
        self.btn_start.pack(side="left", padx=2)
        
        self.btn_reset = self.create_btn(self.btn_row, "↻", self.reset)
        self.btn_reset.pack(side="left", padx=2)
        
        self.btn_close = tk.Button(
            self.btn_row, text="✕", command=self.root.destroy,
            bg="#330000", fg="#FF0000", bd=0, 
            font=("Segoe UI Symbol", 9, "bold"),
            width=3, pady=0,
            activebackground="#550000", activeforeground="red", cursor="hand2"
        )
        self.btn_close.pack(side="left", padx=2)

        # ЭТАЖ 2: МЕТКА ВРЕМЕНИ
        self.start_label = tk.Label(
            self.controls_container,
            text="", 
            font=self.font_meta,
            bg=self.colors["bg"],
            fg=self.colors["meta"]
        )
        # anchor="e" прижимает текст к правому краю (под кнопки)
        self.start_label.pack(side="top", anchor="e", pady=(0, 0))

        self.update_display_text()
        
        # Бинды
        self.time_entry.bind('<Return>', self.on_enter_pressed)
        self.time_entry.bind('<FocusOut>', self.apply_input)
        self.root.bind('<space>', self.on_space_pressed)
        self.time_entry.bind('<space>', self.on_space_pressed) 

        # Перетаскивание
        widgets = [self.root, self.left_frame, self.right_frame, 
                   self.controls_container, self.btn_row, self.start_label]
        for widget in widgets:
            widget.bind('<Button-1>', self.start_move)
            widget.bind('<B1-Motion>', self.do_move)

        self.update_clock()
        self.root.mainloop()

    def create_btn(self, parent, text, command):
        btn = tk.Button(
            parent, text=text, command=command,
            bg=self.colors["btn_bg"], fg=self.colors["btn_text"], bd=0,                       
            font=("Segoe UI Symbol", 9), width=3, pady=0,
            activebackground=self.colors["btn_hover"], cursor="hand2"
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=self.colors["btn_hover"]))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.colors["btn_bg"]))
        return btn

    def format_full(self, total_seconds):
        mins, secs = divmod(total_seconds, 60)
        return f"{mins:02}:{secs:02}"

    def validate_input(self, new_value):
        if new_value == "": return True
        for char in new_value:
            if not (char.isdigit() or char == ":"):
                return False
        return True

    def on_enter_pressed(self, event):
        self.apply_input()
        self.root.focus()
        if not self.running:
            self.toggle()

    def apply_input(self, event=None):
        text = self.time_entry.get().strip()
        
        if not text:
            self.update_display_text()
            return

        try:
            if ":" not in text:
                new_mins = int(text)
                secs = 0
            else:
                parts = text.split(":")
                new_mins = int(parts[0])
                secs = int(parts[1]) if len(parts) > 1 and parts[1] else 0

            if new_mins <= 0 and secs == 0: new_mins = 1
            
            self.minutes = new_mins
            self.seconds = new_mins * 60 + secs
            
            self.update_display_text()
            
            if self.is_paused:
                self.time_entry.config(fg=self.colors["accent"])
            else:
                self.time_entry.config(fg=self.colors["fg"])
            
        except ValueError:
            self.update_display_text()

    def update_display_text(self):
        current_state = self.time_entry.cget('state')
        self.time_entry.config(state='normal')
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, self.format_full(self.seconds))
        if current_state == 'readonly':
            self.time_entry.config(state='readonly')

    def on_space_pressed(self, event):
        if self.time_entry.cget('state') == 'normal':
            self.apply_input()
            self.root.focus()
        self.toggle()
        return "break"

    def toggle(self):
        self.running = not self.running
        
        if self.running:
            self.is_paused = False
            # Если метка пустая, ставим время
            if self.start_label.cget("text") == "":
                current_time = datetime.now().strftime("%H:%M")
                self.start_label.config(text=f"НАЧАЛО: {current_time}")

            if self.time_entry.cget('state') == 'normal':
                self.apply_input()
            self.btn_start.config(text="⏸")
            self.time_entry.config(state="readonly", fg=self.colors["fg"], cursor="arrow")
        else:
            self.is_paused = True
            self.btn_start.config(text="▶")
            self.time_entry.config(state="normal", fg=self.colors["accent"], cursor="xterm")

    def reset(self):
        self.running = False
        self.is_paused = False
        self.seconds = self.minutes * 60
        self.update_display_text()
        self.start_label.config(text="") 
        self.btn_start.config(text="▶")
        self.time_entry.config(state="normal", fg=self.colors["fg"])

    def update_clock(self):
        if self.running and self.seconds > 0:
            self.seconds -= 1
            self.time_entry.config(state='normal')
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, self.format_full(self.seconds))
            self.time_entry.config(state='readonly')
            
        elif self.seconds == 0 and self.running:
            self.running = False
            self.is_paused = False
            self.time_entry.config(state="normal", fg=self.colors["danger"])
            self.btn_start.config(text="■")
            self.root.attributes('-topmost', 0)
            self.root.attributes('-topmost', 1)
            
        self.root.after(1000, self.update_clock)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    app = FocusTimer()