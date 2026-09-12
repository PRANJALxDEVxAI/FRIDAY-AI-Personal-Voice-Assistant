# NOTE - THAT THE FRONTEND IS A AI CREATED AND FORMATED BY ME AS I AM STILL LEARNING FRONTEND




import tkinter as tk
from tkinter import font as tkfont
import threading
import math
import random

from main import listen, process_prompt, speak


# ===============================================================
# FRIDAY // OPTIMIZED SCI-FI INTERFACE
# Designed to stay smooth on low-end hardware.
# ===============================================================

BG = "#05070B"
PANEL = "#0B1018"
PANEL_2 = "#101722"

CYAN = "#49D9FF"
CYAN_DIM = "#17677A"
WHITE = "#EAF7FF"
TEXT_DIM = "#718496"
GREEN = "#55E6A5"
AMBER = "#FFCA62"
PURPLE = "#8B5CFF"
RED = "#FF5D6C"
GRID = "#0D1C29"

STATE_COLORS = {
    "idle": CYAN,
    "listening": GREEN,
    "thinking": AMBER,
    "speaking": PURPLE,
    "error": RED,
}

STATE_HINTS = {
    "idle": "SYSTEM READY  •  CLICK CORE TO SPEAK",
    "listening": "AUDIO INPUT ACTIVE  •  LISTENING",
    "thinking": "NEURAL CORE PROCESSING  •  STAND BY",
    "speaking": "VOICE OUTPUT ACTIVE  •  FRIDAY SPEAKING",
    "error": "SYSTEM ERROR  •  CHECK TERMINAL",
}


class FridayUI:
    def __init__(self, root):
        self.root = root
        self.state = "idle"

        # One lightweight animation loop instead of redrawing
        # hundreds of canvas objects every frame.
        self.phase = 0.0
        self.running = True

        self._create_fonts()

        root.title("FRIDAY // AI CORE")
        root.geometry("1366x768")
        root.minsize(1000, 650)
        root.configure(bg=BG)

        try:
            root.state("zoomed")
        except tk.TclError:
            pass

        self._build_header()
        self._build_main()
        self._build_footer()

        self._create_static_background()
        self._create_core_objects()

        # ~20 FPS. Much lighter than the previous 30+ FPS redraw.
        self.animate()

        root.protocol("WM_DELETE_WINDOW", self.close)

    # -----------------------------------------------------------
    # Fonts
    # -----------------------------------------------------------
    def _create_fonts(self):
        self.font_title = tkfont.Font(
            family="Segoe UI", size=19, weight="bold"
        )
        self.font_small = tkfont.Font(
            family="Consolas", size=9
        )
        self.font_mono = tkfont.Font(
            family="Consolas", size=10, weight="bold"
        )
        self.font_body = tkfont.Font(
            family="Segoe UI", size=11
        )
        self.font_big = tkfont.Font(
            family="Segoe UI", size=24, weight="bold"
        )

    # -----------------------------------------------------------
    # Header
    # -----------------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self.root, bg=BG, height=72)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=BG)
        left.pack(side="left", padx=30, pady=17)

        tk.Label(
            left, text="FRIDAY",
            font=self.font_title,
            fg=WHITE, bg=BG
        ).pack(side="left")

        tk.Label(
            left,
            text="  //  ARTIFICIAL INTELLIGENCE CORE",
            font=self.font_small,
            fg=CYAN, bg=BG
        ).pack(side="left", pady=(7, 0))

        right = tk.Frame(header, bg=BG)
        right.pack(side="right", padx=30)

        self.system_label = tk.Label(
            right,
            text="SYSTEM ONLINE",
            font=self.font_mono,
            fg=GREEN, bg=BG
        )
        self.system_label.pack(side="right")

        self.system_dot = tk.Canvas(
            right, width=14, height=14,
            bg=BG, highlightthickness=0
        )
        self.system_dot.create_oval(
            3, 3, 11, 11,
            fill=GREEN, outline=""
        )
        self.system_dot.pack(side="right", padx=(0, 9))

        tk.Frame(
            self.root, bg=CYAN_DIM, height=1
        ).pack(fill="x")

    # -----------------------------------------------------------
    # Main layout
    # -----------------------------------------------------------
    def _build_main(self):
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(fill="both", expand=True)

        self.left_hud = tk.Frame(
            self.main, bg=BG, width=245
        )
        self.left_hud.pack(
            side="left", fill="y",
            padx=(24, 5), pady=24
        )
        self.left_hud.pack_propagate(False)
        self._build_left_hud()

        self.center = tk.Frame(self.main, bg=BG)
        self.center.pack(
            side="left", fill="both", expand=True,
            padx=8, pady=18
        )
        self._build_core()

        self.right_hud = tk.Frame(
            self.main, bg=BG, width=285
        )
        self.right_hud.pack(
            side="right", fill="y",
            padx=(5, 24), pady=24
        )
        self.right_hud.pack_propagate(False)
        self._build_right_hud()

    # -----------------------------------------------------------
    # Panel helper
    # -----------------------------------------------------------
    def _panel(self, parent, title, height):
        frame = tk.Frame(
            parent,
            bg=PANEL,
            height=height,
            highlightbackground="#142331",
            highlightthickness=1
        )
        frame.pack(fill="x", pady=(0, 14))
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            font=self.font_small,
            fg=CYAN, bg=PANEL,
            anchor="w"
        ).pack(
            fill="x", padx=14, pady=(11, 8)
        )

        tk.Frame(
            frame, bg="#132331", height=1
        ).pack(fill="x")

        return frame

    # -----------------------------------------------------------
    # Left HUD
    # -----------------------------------------------------------
    def _build_left_hud(self):
        panel = self._panel(
            self.left_hud, "CORE STATUS", 155
        )

        self.status_text = tk.Label(
            panel,
            text="IDLE",
            font=self.font_big,
            fg=CYAN, bg=PANEL
        )
        self.status_text.pack(pady=(14, 2))

        self.status_hint = tk.Label(
            panel,
            text="READY",
            font=self.font_small,
            fg=TEXT_DIM, bg=PANEL
        )
        self.status_hint.pack()

        panel2 = self._panel(
            self.left_hud, "SYSTEM TELEMETRY", 190
        )

        for name, value in [
            ("AUDIO", "READY"),
            ("NEURAL", "ONLINE"),
            ("VOICE", "ONLINE"),
            ("MEMORY", "JSON"),
            ("CORE", "ACTIVE"),
        ]:
            self._telemetry_row(panel2, name, value)

        panel3 = self._panel(
            self.left_hud, "INTERFACE", 135
        )

        tk.Label(
            panel3,
            text="CLICK THE CORE",
            font=self.font_mono,
            fg=WHITE, bg=PANEL
        ).pack(pady=(17, 5))

        tk.Label(
            panel3,
            text="Speak naturally.\nFriday will respond.",
            font=self.font_small,
            fg=TEXT_DIM, bg=PANEL,
            justify="center"
        ).pack()

    def _telemetry_row(self, parent, name, value):
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill="x", padx=14, pady=5)

        tk.Label(
            row, text=name,
            font=self.font_small,
            fg=TEXT_DIM, bg=PANEL
        ).pack(side="left")

        tk.Label(
            row, text=value,
            font=self.font_small,
            fg=GREEN, bg=PANEL
        ).pack(side="right")

    # -----------------------------------------------------------
    # Core
    # -----------------------------------------------------------
    def _build_core(self):
        self.core_canvas = tk.Canvas(
            self.center,
            bg=BG,
            highlightthickness=0,
            cursor="hand2"
        )
        self.core_canvas.pack(fill="both", expand=True)

        self.core_canvas.bind(
            "<ButtonPress-1>",
            self._on_core_press
        )
        self.core_canvas.bind(
            "<ButtonRelease-1>",
            self.on_core_release
        )

    def _create_static_background(self):
        canvas = self.core_canvas

        # Static grid. It does NOT get redrawn every frame.
        width = max(canvas.winfo_width(), 700)
        height = max(canvas.winfo_height(), 500)

        for y in range(35, height, 55):
            canvas.create_line(
                0, y, width, y,
                fill=GRID, width=1,
                tags="static"
            )

        for x in range(30, width, 80):
            canvas.create_line(
                x, 0, x, height,
                fill="#08131D", width=1,
                tags="static"
            )

        # A few static stars instead of 95 animated stars.
        random.seed(7)

        for _ in range(35):
            x = random.randint(20, width - 20)
            y = random.randint(20, height - 20)
            r = random.choice([1, 1, 1, 2])

            canvas.create_oval(
                x-r, y-r, x+r, y+r,
                fill="#1B4354",
                outline="",
                tags="static"
            )

    def _create_core_objects(self):
        c = self.core_canvas

        # These objects are created ONCE and only moved/configured.
        self.core_items = {}

        for i in range(3):
            self.core_items[f"outer{i}"] = c.create_oval(
                0, 0, 0, 0,
                outline=CYAN_DIM,
                width=1,
                tags="core"
            )

        for i in range(2):
            self.core_items[f"arc{i}"] = c.create_arc(
                0, 0, 0, 0,
                start=0, extent=90,
                style="arc",
                outline=CYAN,
                width=2,
                tags="core"
            )

        self.core_items["sphere"] = c.create_oval(
            0, 0, 0, 0,
            fill="#08121B",
            outline=CYAN,
            width=2,
            tags="core"
        )

        self.core_items["inner1"] = c.create_oval(
            0, 0, 0, 0,
            outline="#12394A",
            width=1,
            tags="core"
        )

        self.core_items["inner2"] = c.create_oval(
            0, 0, 0, 0,
            outline="#12394A",
            width=1,
            tags="core"
        )

        self.core_items["reactor"] = c.create_oval(
            0, 0, 0, 0,
            fill="#0D1B25",
            outline=CYAN,
            width=2,
            tags="core"
        )

        self.core_items["glow"] = c.create_oval(
            0, 0, 0, 0,
            fill=CYAN,
            outline="",
            tags="core"
        )

        self.core_items["title"] = c.create_text(
            0, 0,
            text="FRIDAY",
            font=self.font_mono,
            fill=WHITE,
            tags="core"
        )

        self.core_items["hint"] = c.create_text(
            0, 0,
            text="SYSTEM READY",
            font=self.font_small,
            fill=CYAN,
            tags="core"
        )

        # Eight particles, also created only once.
        self.particles = []

        for _ in range(8):
            item = c.create_oval(
                0, 0, 0, 0,
                fill=CYAN,
                outline="",
                tags="core"
            )
            self.particles.append(item)

    def _update_core(self):
        c = self.core_canvas

        width = max(c.winfo_width(), 700)
        height = max(c.winfo_height(), 500)

        cx = width / 2
        cy = height / 2 - 10

        color = STATE_COLORS.get(
            self.state, CYAN
        )

        pulse = (
            math.sin(self.phase * 2.0) + 1
        ) / 2

        if self.state == "idle":
            energy = 7
        elif self.state == "listening":
            energy = 17
        elif self.state == "thinking":
            energy = 12
        elif self.state == "speaking":
            energy = 20
        else:
            energy = 8

        # Three breathing rings.
        for i in range(3):
            radius = (
                155 + i * 27
                + pulse * energy
            )

            c.coords(
                self.core_items[f"outer{i}"],
                cx-radius, cy-radius,
                cx+radius, cy+radius
            )

            c.itemconfig(
                self.core_items[f"outer{i}"],
                outline=(
                    CYAN_DIM
                    if i < 2
                    else "#102431"
                )
            )

        # Two rotating arcs.
        for i in range(2):
            radius = 145 + i * 22
            start = (
                self.phase * (65 + i * 25)
                + i * 180
            ) % 360

            c.coords(
                self.core_items[f"arc{i}"],
                cx-radius,
                cy-radius * 0.48,
                cx+radius,
                cy+radius * 0.48
            )

            c.itemconfig(
                self.core_items[f"arc{i}"],
                start=start,
                extent=95,
                outline=color
            )

        # Main sphere.
        radius = 103 + pulse * energy * 0.3

        c.coords(
            self.core_items["sphere"],
            cx-radius, cy-radius,
            cx+radius, cy+radius
        )

        c.itemconfig(
            self.core_items["sphere"],
            outline=color
        )

        # Two latitude-style arcs.
        r = radius

        c.coords(
            self.core_items["inner1"],
            cx-r,
            cy-35,
            cx+r,
            cy+35
        )

        c.coords(
            self.core_items["inner2"],
            cx-55,
            cy-r,
            cx+55,
            cy+r
        )

        # Reactor.
        rr = 30 + pulse * 5

        c.coords(
            self.core_items["reactor"],
            cx-rr, cy-rr,
            cx+rr, cy+rr
        )

        c.itemconfig(
            self.core_items["reactor"],
            outline=color
        )

        # Bright center.
        glow = 11 + pulse * 4

        c.coords(
            self.core_items["glow"],
            cx-glow, cy-glow,
            cx+glow, cy+glow
        )

        c.itemconfig(
            self.core_items["glow"],
            fill=color
        )

        # Orbiting particles.
        for i, item in enumerate(self.particles):
            angle = (
                self.phase * 0.8
                + i * math.pi / 4
            )

            orbit = 142 + (i % 2) * 22

            x = cx + math.cos(angle) * orbit
            y = cy + math.sin(angle) * orbit * 0.58

            size = 2 if i % 2 else 3

            c.coords(
                item,
                x-size, y-size,
                x+size, y+size
            )

            c.itemconfig(
                item,
                fill=color
            )

        c.coords(
            self.core_items["title"],
            cx, cy + 132
        )

        c.coords(
            self.core_items["hint"],
            cx, cy + 151
        )

        c.itemconfig(
            self.core_items["hint"],
            text=self.state.upper(),
            fill=color
        )

    # -----------------------------------------------------------
    # Lightweight neural activity
    # -----------------------------------------------------------
    def _build_right_hud(self):
        panel = self._panel(
            self.right_hud, "NEURAL ACTIVITY", 150
        )

        self.activity_canvas = tk.Canvas(
            panel,
            bg=PANEL,
            height=95,
            highlightthickness=0
        )
        self.activity_canvas.pack(
            fill="x", padx=10, pady=10
        )

        self.activity_lines = []

        # Only 30 bars, created once.
        for _ in range(30):
            item = self.activity_canvas.create_line(
                0, 47, 0, 47,
                fill=CYAN,
                width=2
            )
            self.activity_lines.append(item)

        panel2 = self._panel(
            self.right_hud, "LAST RESPONSE", 225
        )

        self.response_label = tk.Label(
            panel2,
            text="Awaiting command...",
            font=self.font_body,
            fg=TEXT_DIM,
            bg=PANEL,
            wraplength=240,
            justify="left",
            anchor="nw"
        )
        self.response_label.pack(
            fill="both", expand=True,
            padx=14, pady=14
        )

        panel3 = self._panel(
            self.right_hud, "CONTROLS", 135
        )

        self.clear_btn = tk.Button(
            panel3,
            text="CLEAR TRANSCRIPT",
            font=self.font_small,
            fg=WHITE,
            bg=PANEL_2,
            activebackground="#172638",
            activeforeground=CYAN,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.clear_transcript
        )
        self.clear_btn.pack(
            fill="x", padx=14,
            pady=(15, 7), ipady=7
        )

        tk.Label(
            panel3,
            text="Conversation saved to JSON.",
            font=self.font_small,
            fg=TEXT_DIM,
            bg=PANEL
        ).pack()

    def _update_activity(self):
        width = max(
            self.activity_canvas.winfo_width(),
            230
        )

        color = STATE_COLORS.get(
            self.state, CYAN
        )

        if self.state == "idle":
            amplitude = 4
        elif self.state == "listening":
            amplitude = 17
        elif self.state == "thinking":
            amplitude = 10
        elif self.state == "speaking":
            amplitude = 23
        else:
            amplitude = 5

        bar_width = width / len(self.activity_lines)

        for i, item in enumerate(self.activity_lines):
            x = i * bar_width + bar_width / 2

            value = math.sin(
                self.phase * 4 + i * 0.55
            )

            value += 0.25 * math.sin(
                self.phase * 7 + i
            )

            y = 47 + value * amplitude

            self.activity_canvas.coords(
                item,
                x, 47,
                x, y
            )

            self.activity_canvas.itemconfig(
                item,
                fill=color
            )

    # -----------------------------------------------------------
    # Footer
    # -----------------------------------------------------------
    def _build_footer(self):
        footer = tk.Frame(
            self.root,
            bg=BG,
            height=54
        )
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        tk.Frame(
            footer, bg=CYAN_DIM, height=1
        ).pack(fill="x")

        tk.Label(
            footer,
            text=(
                "FRIDAY CORE  •  GEMINI  •  "
                "SPEECH RECOGNITION  •  PYTTSX3"
            ),
            font=self.font_small,
            fg=TEXT_DIM,
            bg=BG
        ).pack(side="left", padx=30, pady=17)

        self.footer_status = tk.Label(
            footer,
            text="SYSTEM READY",
            font=self.font_small,
            fg=GREEN,
            bg=BG
        )
        self.footer_status.pack(
            side="right", padx=30
        )

    # -----------------------------------------------------------
    # Animation loop
    # -----------------------------------------------------------
    def animate(self):
        if not self.running:
            return

        self.phase += 0.055

        self._update_core()
        self._update_activity()

        # 50 ms = 20 FPS.
        # Much lighter on CPU/GPU than constantly creating/deleting
        # hundreds of Canvas objects.
        self.root.after(50, self.animate)

    # -----------------------------------------------------------
    # Status
    # -----------------------------------------------------------
    def set_status(self, state):
        self.state = state

        color = STATE_COLORS.get(
            state, CYAN
        )

        self.status_text.config(
            text=state.upper(),
            fg=color
        )

        self.status_hint.config(
            text=STATE_HINTS.get(state, ""),
            fg=color
        )

        self.footer_status.config(
            text=STATE_HINTS.get(state, ""),
            fg=color
        )

        if state == "error":
            self.system_label.config(
                text="SYSTEM ALERT",
                fg=RED
            )
        else:
            self.system_label.config(
                text="SYSTEM ONLINE",
                fg=GREEN
            )

    # -----------------------------------------------------------
    # Interaction
    # -----------------------------------------------------------
    def _on_core_press(self, event=None):
        self.set_status("listening")

    def on_core_release(self, event=None):
        worker = threading.Thread(
            target=self.process_command,
            daemon=True
        )
        worker.start()

    # -----------------------------------------------------------
    # Backend
    # -----------------------------------------------------------
    def process_command(self):
        try:
            self.root.after(
                0, self.set_status, "listening"
            )

            prompt = listen()

            if not prompt:
                self.root.after(
                    0, self.set_status, "idle"
                )
                return

            self.root.after(
                0,
                self.append_transcript,
                "you",
                prompt
            )

            self.root.after(
                0, self.set_status, "thinking"
            )

            # Gemini + conversation JSON storage
            answer = process_prompt(prompt)

            self.root.after(
                0,
                self.append_transcript,
                "friday",
                answer
            )

            self.root.after(
                0,
                self.update_response,
                answer
            )

            self.root.after(
                0, self.set_status, "speaking"
            )

            speak(answer)

            self.root.after(
                0, self.set_status, "idle"
            )

        except Exception as e:
            print(f"Friday error: {e}")

            self.root.after(
                0, self.set_status, "error"
            )

            self.root.after(
                0,
                self.update_response,
                "Sorry, something went wrong."
            )

    # -----------------------------------------------------------
    # Transcript / response
    # -----------------------------------------------------------
    def append_transcript(self, who, text):
        # Keep the main UI lightweight: latest conversation is shown
        # in the response panel. The full conversation remains in JSON.
        if who == "friday":
            self.update_response(text)

    def update_response(self, text):
        self.response_label.config(
            text=text,
            fg=WHITE
        )

    def clear_transcript(self):
        self.response_label.config(
            text="Awaiting command...",
            fg=TEXT_DIM
        )
        self.set_status("idle")

    # -----------------------------------------------------------
    # Close
    # -----------------------------------------------------------
    def close(self):
        self.running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FridayUI(root)
    root.mainloop()
