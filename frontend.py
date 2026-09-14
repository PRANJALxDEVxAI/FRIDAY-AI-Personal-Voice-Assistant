import sys
import threading
import time
import math
from main import listen, handle_prompt, speak

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QRadialGradient
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class CoreWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = "IDLE"
        self.phase = 0.0
        self.setMinimumSize(420, 420)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def set_state(self, state):
        self.state = state.upper()
        self.update()

    def animate(self):
        self.phase += 0.035
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx = self.width() / 2
        cy = self.height() / 2
        base_radius = min(self.width(), self.height()) * 0.19

        colors = {
            "IDLE": QColor("#49D9FF"),
            "LISTENING": QColor("#55E6A5"),
            "THINKING": QColor("#FFCA62"),
            "SPEAKING": QColor("#8B5CFF"),
            "ERROR": QColor("#FF5D6C"),
        }

        color = colors.get(self.state, colors["IDLE"])

        # Background glow
        gradient = QRadialGradient(cx, cy, base_radius * 3.2)
        glow = QColor(color)
        glow.setAlpha(70)
        gradient.setColorAt(0.0, glow)
        glow2 = QColor(color)
        glow2.setAlpha(0)
        gradient.setColorAt(1.0, glow2)

        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            int(cx - base_radius * 3.2),
            int(cy - base_radius * 3.2),
            int(base_radius * 6.4),
            int(base_radius * 6.4),
        )

        # Animated rings
        for i in range(4):
            radius = base_radius + i * 30 + math.sin(self.phase + i) * 5

            pen = QPen(color)
            pen.setWidth(2 if i < 2 else 1)
            pen.setColor(QColor(color.red(), color.green(), color.blue(),
                                max(45, 150 - i * 30)))

            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            painter.drawEllipse(
                int(cx - radius),
                int(cy - radius),
                int(radius * 2),
                int(radius * 2),
            )

        # Rotating scanner arc
        pen = QPen(color)
        pen.setWidth(4)
        painter.setPen(pen)

        start_angle = int((self.phase * 180 / math.pi) * 16)
        painter.drawArc(
            int(cx - base_radius * 2.0),
            int(cy - base_radius * 2.0),
            int(base_radius * 4.0),
            int(base_radius * 4.0),
            start_angle,
            95 * 16,
        )

        # Core
        core_gradient = QRadialGradient(cx, cy, base_radius)
        core_gradient.setColorAt(0.0, QColor("#EAF7FF"))
        core_gradient.setColorAt(0.18, color)
        dark = QColor(color)
        dark.setAlpha(80)
        core_gradient.setColorAt(1.0, dark)

        painter.setBrush(core_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            int(cx - base_radius),
            int(cy - base_radius),
            int(base_radius * 2),
            int(base_radius * 2),
        )

        # Center label
        painter.setPen(QColor("#EAF7FF"))
        painter.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        text_rect = painter.boundingRect(
            int(cx - 100), int(cy - 20), 200, 40,
            Qt.AlignmentFlag.AlignCenter,
            "FRIDAY",
        )
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, "FRIDAY")


class Worker(QObject):
    status = pyqtSignal(str)
    user_text = pyqtSignal(str)
    friday_text = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        try:
            while self.running:
                self.status.emit("LISTENING")

                prompt = listen()

                if not self.running:
                    break

                if not prompt:
                    continue

                self.user_text.emit(prompt)

                self.status.emit("THINKING")

                answer = handle_prompt(prompt)

                self.friday_text.emit(answer)

                self.status.emit("SPEAKING")

                speak(answer)

                # After speaking, automatically return to listening.
                self.status.emit("LISTENING")

        except Exception as error:
            print(f"FRIDAY error: {error}")
            self.status.emit("ERROR")

        self.finished.emit()

    def stop(self):
        self.running = False


class FridayUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FRIDAY AI")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 760)

        self.worker = None
        self.worker_thread = None

        self.build_ui()
        self.start_voice_thread()

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(18, 18, 18, 14)
        main_layout.setSpacing(12)

        self.setStyleSheet("""
            QWidget {
                background-color: #05070B;
                color: #EAF7FF;
                font-family: "Segoe UI";
            }

            QFrame#panel {
                background-color: #0B1018;
                border: 1px solid #162431;
                border-radius: 10px;
            }

            QLabel#title {
                color: #49D9FF;
                font-size: 22px;
                font-weight: bold;
                letter-spacing: 2px;
            }

            QLabel#status {
                color: #55E6A5;
                font-size: 13px;
                font-weight: bold;
            }

            QLabel#section {
                color: #49D9FF;
                font-size: 12px;
                font-weight: bold;
            }

            QTextEdit {
                background-color: #070B11;
                border: 1px solid #162431;
                border-radius: 8px;
                padding: 10px;
                color: #B9CBD8;
                font-size: 12px;
            }

            QLineEdit {
                background-color: #070B11;
                border: 1px solid #1D3442;
                border-radius: 7px;
                padding: 10px;
                color: #EAF7FF;
            }

            QPushButton {
                background-color: #0D1C29;
                border: 1px solid #17677A;
                border-radius: 7px;
                padding: 9px 16px;
                color: #49D9FF;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #102938;
            }
        """)

        # Header
        header = QFrame()
        header.setObjectName("panel")
        header_layout = QHBoxLayout(header)

        title = QLabel("F.R.I.D.A.Y")
        title.setObjectName("title")

        subtitle = QLabel("PERSONAL AI ASSISTANT")
        subtitle.setStyleSheet("color: #718496; font-size: 10px;")

        self.status_label = QLabel("● SYSTEM ONLINE")
        self.status_label.setObjectName("status")

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addStretch()
        header_layout.addWidget(self.status_label)

        main_layout.addWidget(header)

        # Main area
        content = QHBoxLayout()
        content.setSpacing(12)

        # Left panel
        left = QFrame()
        left.setObjectName("panel")
        left_layout = QVBoxLayout(left)

        section = QLabel("SYSTEM STATUS")
        section.setObjectName("section")
        left_layout.addWidget(section)

        for text in [
            "● VOICE INPUT       ONLINE",
            "● GEMINI CORE       ONLINE",
            "● TEXT TO SPEECH    ONLINE",
            "● CONVERSATION      ACTIVE",
            "● OS CONTROL        READY",
            "● EMAIL SYSTEM      READY",
        ]:
            label = QLabel(text)
            label.setStyleSheet("color: #718496; padding: 7px 2px;")
            left_layout.addWidget(label)

        left_layout.addStretch()

        hint = QLabel("ALWAYS LISTENING\n\nSpeak naturally.\nFRIDAY will respond.")
        hint.setStyleSheet("color: #49D9FF; font-size: 12px;")
        left_layout.addWidget(hint)

        content.addWidget(left, 1)

        # Center
        center = QFrame()
        center.setObjectName("panel")
        center_layout = QVBoxLayout(center)

        core_title = QLabel("FRIDAY NEURAL CORE")
        core_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        core_title.setObjectName("section")

        self.core = CoreWidget()
        center_layout.addWidget(core_title)
        center_layout.addWidget(self.core, 1)

        self.state_label = QLabel("SYSTEM READY • ALWAYS LISTENING")
        self.state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.state_label.setStyleSheet(
            "color: #718496; font-size: 11px; padding: 8px;"
        )

        center_layout.addWidget(self.state_label)
        content.addWidget(center, 2)

        # Right panel
        right = QFrame()
        right.setObjectName("panel")
        right_layout = QVBoxLayout(right)

        activity_title = QLabel("FRIDAY ACTIVITY")
        activity_title.setObjectName("section")
        right_layout.addWidget(activity_title)

        self.activity = QTextEdit()
        self.activity.setReadOnly(True)
        right_layout.addWidget(self.activity, 1)

        content.addWidget(right, 1)

        main_layout.addLayout(content, 1)

        # Bottom input
        bottom = QFrame()
        bottom.setObjectName("panel")
        bottom_layout = QHBoxLayout(bottom)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type a command to FRIDAY...")
        self.input_box.returnPressed.connect(self.send_text_command)

        send_button = QPushButton("SEND")
        send_button.clicked.connect(self.send_text_command)

        bottom_layout.addWidget(self.input_box, 1)
        bottom_layout.addWidget(send_button)

        main_layout.addWidget(bottom)

        footer = QLabel(
            "MIC • ALWAYS LISTENING        GEMINI • CONNECTED        "
            "OS • READY        MAIL • READY"
        )
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #17677A; font-size: 10px;")

        main_layout.addWidget(footer)

    def start_voice_thread(self):
        self.worker_thread = threading.Thread(
            target=self.voice_loop,
            daemon=True
        )
        self.worker_thread.start()

    def voice_loop(self):
        worker = Worker()
        self.worker = worker

        worker.status.connect(self.update_status)
        worker.user_text.connect(self.show_user)
        worker.friday_text.connect(self.show_friday)

        worker.run()

    def update_status(self, state):
        self.core.set_state(state)

        hints = {
            "LISTENING": "AUDIO INPUT ACTIVE • LISTENING",
            "THINKING": "NEURAL CORE PROCESSING • STAND BY",
            "SPEAKING": "VOICE OUTPUT ACTIVE • FRIDAY SPEAKING",
            "ERROR": "SYSTEM ERROR • CHECK TERMINAL",
        }

        state = state.upper()
        self.state_label.setText(
            hints.get(state, "SYSTEM READY • ALWAYS LISTENING")
        )

        status_colors = {
            "LISTENING": "#55E6A5",
            "THINKING": "#FFCA62",
            "SPEAKING": "#8B5CFF",
            "ERROR": "#FF5D6C",
        }

        color = status_colors.get(state, "#49D9FF")
        self.status_label.setStyleSheet(
            f"color: {color}; font-size: 13px; font-weight: bold;"
        )

    def show_user(self, text):
        self.activity.append(f"<b style='color:#55E6A5'>YOU:</b> {text}")

    def show_friday(self, text):
        safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.activity.append(
            f"<b style='color:#49D9FF'>FRIDAY:</b> {safe_text}"
        )

    def send_text_command(self):
        text = self.input_box.text().strip()

        if not text:
            return

        self.input_box.clear()
        self.show_user(text)
        self.update_status("THINKING")

        def process():
            try:
                answer = handle_prompt(text)
                self.show_friday(answer)
                self.update_status("SPEAKING")
                speak(answer)
                self.update_status("LISTENING")
            except Exception as error:
                print(f"Text command error: {error}")
                self.update_status("ERROR")

        threading.Thread(target=process, daemon=True).start()

    def closeEvent(self, event):
        if self.worker:
            self.worker.stop()

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FridayUI()
    window.show()
    sys.exit(app.exec())
