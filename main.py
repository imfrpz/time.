import tkinter as tk
from tkinter import font
from datetime import datetime
import winsound

class VisualAlert:
    def __init__(self):
        self.overlay = None
        self.is_active = False

    def show(self, color="red"):
        if self.overlay: self.stop()
        self.overlay = tk.Toplevel()
        w, h = self.overlay.winfo_screenwidth(), self.overlay.winfo_screenheight()
        self.overlay.geometry(f"{w}x{h}+0+0")
        self.overlay.overrideredirect(True)
        self.overlay.attributes('-topmost', True, '-transparentcolor', 'white')
        
        self.canvas = tk.Canvas(self.overlay, width=w, height=h, highlightthickness=0, bg='white')
        self.canvas.pack()
        self.canvas.create_rectangle(2, 2, w-2, h-2, outline=color, width=3, tags="border")
        
        self.is_active = True
        self.cycle()

    def cycle(self):
        if not self.overlay or not self.is_active: return
        curr = self.canvas.itemcget("border", "state")
        new_s = "hidden" if curr == "normal" else "normal"
        self.canvas.itemconfig("border", state=new_s)
        if new_s == "normal" and self.canvas.itemcget("border", "outline") == "red":
            winsound.Beep(1000, 150)
        self.overlay.after(500, self.cycle)

    def stop(self):
        self.is_active = False
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None

class FocusTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.alert = VisualAlert()
        self.minutes, self.seconds = 90, 5400
        self.running = False
        
        self.colors = {
            "bg": "#000000", "fg": "#FFFFFF", "accent": "#FFD700",
            "danger": "#FF4444", "success": "#00FF00", "btn": "#1A1A1A", "meta": "#666666"
        }

        # ГЕОМЕТРИЯ: Центр-Верх
        w_width, w_height = 260, 70
        s_width = self.root.winfo_screenwidth()
        pos_x = (s_width // 2) - (w_width // 2)
        
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True, '-alpha', 0.9)
        self.root.geometry(f"{w_width}x{w_height}+{pos_x}+0")
        self.root.configure(bg=self.colors["bg"])

        self.font_timer = font.Font(family="Consolas", size=32, weight="normal")
        self.font_btn = font.Font(family="Segoe UI Symbol", size=10)
        self.font_meta = font.Font(family="Consolas", size=8, weight="bold")

        self.setup_ui()
        self.setup_binds()
        self.update_display_text()
        self.update_clock()
        
        self.root.after(100, lambda: self.root.focus_set())
        self.root.mainloop()

    def setup_ui(self):
        self.main_wrapper = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_wrapper.pack(fill="both", expand=True, padx=10)

        self.time_entry = tk.Entry(
            self.main_wrapper, font=self.font_timer, bg=self.colors["bg"], fg=self.colors["fg"],
            bd=0, justify='left', width=5, insertbackground="#FFFFFF",
            readonlybackground=self.colors["bg"], disabledforeground=self.colors["fg"], 
            highlightthickness=0
        )
        self.time_entry.pack(side="left", anchor="center")

        self.control_block = tk.Frame(self.main_wrapper, bg=self.colors["bg"])
        self.control_block.pack(side="right", anchor="center")

        self.btn_row = tk.Frame(self.control_block, bg=self.colors["bg"])
        self.btn_row.pack(side="top")

        btn_specs = [
            ("✓", self.complete_early, self.colors["success"]),
            ("▶", self.toggle, self.colors["fg"]),
            ("↻", self.reset, self.colors["fg"]),
            ("✕", self.root.destroy, self.colors["danger"])
        ]

        self.btns = []
        for text, cmd, fg in btn_specs:
            b = tk.Button(self.btn_row, text=text, command=cmd, 
                         bg=self.colors["btn"], fg=fg, bd=0, 
                         font=self.font_btn, width=2, height=1, 
                         activebackground="#333333", activeforeground=fg, 
                         cursor="hand2", takefocus=False)
            b.pack(side="left", padx=1)
            self.btns.append(b)
        
        self.btn_start = self.btns[1]

        self.status_label = tk.Label(self.control_block, text="", font=self.font_meta, 
                                   bg=self.colors["bg"], fg=self.colors["meta"])
        self.status_label.pack(side="top", anchor="e", pady=(2, 0))

    def toggle(self, event=None):
        if not self.running:
            self.apply_input()
            self.running, self.btn_start['text'] = True, "⏸"
            self.alert.stop()
            self.status_label.config(text=f"START: {datetime.now().strftime('%H:%M')}", fg=self.colors["meta"])
            self.time_entry.config(state="readonly", fg=self.colors["fg"])
            self.root.focus_set() 
        else:
            self.running, self.btn_start['text'] = False, "▶"
            self.time_entry.config(state="normal", fg=self.colors["accent"])
        return "break"

    def complete_early(self, event=None):
        if not self.running and self.seconds == (self.minutes * 60): return
        self.running = False
        self.alert.show(color="green")
        self.time_entry.config(state="normal", fg=self.colors["success"])
        self.status_label.config(text="TASK COMPLETED", fg=self.colors["success"])
        self.btn_start.config(text="▶")
        self.root.focus_set()

    def apply_input(self):
        try:
            val = self.time_entry.get()
            m, s = map(int, val.split(":")) if ":" in val else (int(val), 0)
            self.seconds = self.minutes = m * 60 + s
        except: pass

    def update_clock(self):
        if self.running and self.seconds > 0:
            self.seconds -= 1
            self.update_display_text()
        elif self.seconds == 0 and self.running:
            self.running = False
            self.alert.show(color="red")
            self.time_entry.config(state="normal", fg=self.colors["danger"])
            self.status_label.config(text="TIME IS UP", fg=self.colors["danger"])
            self.btn_start.config(text="■")
        self.root.after(1000, self.update_clock)

    def reset(self):
        self.alert.stop()
        self.running, self.seconds = False, self.minutes
        self.update_display_text()
        self.status_label.config(text="", fg=self.colors["meta"]) 
        self.btn_start.config(text="▶")
        self.time_entry.config(state="normal", fg=self.colors["fg"])
        self.root.focus_set()

    def update_display_text(self):
        st = self.time_entry.cget('state')
        self.time_entry.config(state='normal')
        self.time_entry.delete(0, tk.END)
        m, s = divmod(self.seconds, 60)
        self.time_entry.insert(0, f"{m:02}:{s:02}")
        self.time_entry.config(state=st)

    def setup_binds(self):
        for w in [self.main_wrapper, self.control_block, self.status_label, self.btn_row]:
            w.bind('<Button-1>', self.on_bg_click)
            w.bind('<B1-Motion>', self.do_move)
        self.root.bind('<Button-1>', self.on_bg_click)
        self.time_entry.bind('<Return>', self.toggle)
        self.root.bind('<Control-Return>', self.complete_early)
        self.root.bind('<space>', self.toggle)

    def on_bg_click(self, event):
        if event.widget != self.time_entry:
            self.root.focus_set()
        self.start_move(event)

    def start_move(self, event): self.x, self.y = event.x, event.y
    def do_move(self, event):
        x, y = self.root.winfo_x() + (event.x-self.x), self.root.winfo_y() + (event.y-self.y)
        self.root.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    FocusTimer()