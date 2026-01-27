from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Charts(QWidget):
    def __init__(self):
        super().__init__()
        self.summary = None
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QLabel#CardTitle {
                font-size: 16px;
                font-weight: 600;
                color: #0f172a;
            }

            QLabel#Icon {
                color: #2563eb;
                font-size: 16px;
            }

            QFrame#Card {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
        """)

        self.root = QHBoxLayout(self)
        self.root.setSpacing(24)

        self.pie_card = self.create_card("📊", "Equipment Type Distribution")
        self.bar_card = self.create_card("📈", "Average Parameters")

        self.root.addWidget(self.pie_card)
        self.root.addWidget(self.bar_card)

        self.render_placeholder()

    # ---------------- UI Helpers ----------------
    def create_card(self, icon, title_text):
        card = QFrame()
        card.setObjectName("Card")

        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        header = QHBoxLayout()
        header.setSpacing(8)

        icon_label = QLabel(icon)
        icon_label.setObjectName("Icon")

        title = QLabel(title_text)
        title.setObjectName("CardTitle")

        header.addWidget(icon_label)
        header.addWidget(title)
        header.addStretch()

        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        canvas.setMinimumHeight(260)

        layout.addLayout(header)
        layout.addWidget(canvas)

        card.canvas = canvas
        card.figure = canvas.figure

        return card

    # ---------------- Placeholder (Skeleton) ----------------
    def render_placeholder(self):
        for card in [self.pie_card, self.bar_card]:
            fig = card.figure
            fig.clear()
            ax = fig.add_subplot(111)

            ax.set_facecolor("#e5e7eb")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.text(
                0.5, 0.5, "Loading…",
                ha="center", va="center",
                fontsize=12, color="#64748b"
            )

            card.canvas.draw()

    # ---------------- Update Charts ----------------
    def update(self, summary):
        self.summary = summary

        if not summary:
            self.render_placeholder()
            return

        self.render_pie_chart()
        self.render_bar_chart()

    # ---------------- Pie Chart ----------------
    def render_pie_chart(self):
        fig = self.pie_card.figure
        fig.clear()
        ax = fig.add_subplot(111)

        labels = list(self.summary.type_distribution.keys())
        values = list(self.summary.type_distribution.values())

        colors = [
            "#2563eb", "#0d9488", "#f59e0b",
            "#7c3aed", "#16a34a"
        ]

        ax.pie(
            values,
            labels=labels,
            autopct="%1.0f%%",
            startangle=140,
            colors=colors,
            textprops={"fontsize": 10},
        )

        ax.axis("equal")
        fig.tight_layout()
        self.pie_card.canvas.draw()

    # ---------------- Bar Chart ----------------
    def render_bar_chart(self):
        fig = self.bar_card.figure
        fig.clear()
        ax = fig.add_subplot(111)

        labels = ["Flowrate", "Pressure", "Temperature"]
        values = [
            self.summary.avg_flowrate,
            self.summary.avg_pressure,
            self.summary.avg_temperature,
        ]

        colors = ["#38bdf8", "#f59e0b", "#ef4444"]

        bars = ax.bar(labels, values, color=colors)

        ax.set_ylabel("Value")
        ax.set_ylim(bottom=0)
        ax.grid(axis="y", color="#e5e7eb")
        ax.set_axisbelow(True)

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.1f}",
                ha="center",
                va="bottom",
                fontsize=10,
            )

        fig.tight_layout()
        self.bar_card.canvas.draw()
