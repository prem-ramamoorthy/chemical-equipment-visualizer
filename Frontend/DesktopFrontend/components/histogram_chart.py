from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QSizePolicy
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

@dataclass
class HistogramData:
    labels: List[str]
    flowrate: List[float]
    temperature: List[float]

@dataclass
class ChartsGridSummary:
    histogram: HistogramData

def make_card_frame() -> QFrame:
    card = QFrame()
    card.setObjectName("Card")
    card.setStyleSheet("""
        QFrame#Card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
        }
    """)
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(18)
    shadow.setOffset(0, 6)
    shadow.setColor(QColor(15, 23, 42, 35))
    card.setGraphicsEffect(shadow)
    return card

def title_label(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(11)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color: #0f172a;")
    lbl.setWordWrap(True)
    return lbl

def icon_badge(text: str = "▮") -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(12)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color: #2563eb;")
    lbl.setFixedWidth(16)
    lbl.setAlignment(Qt.AlignCenter)
    return lbl

class HistogramChartWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._card = make_card_frame()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self._card)
        lay = QVBoxLayout(self._card)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)
        header = QHBoxLayout()
        header.setSpacing(8)
        header.addWidget(icon_badge("▮"))
        header.addWidget(title_label("Parameter Distribution"))
        header.addStretch(1)
        lay.addLayout(header)
        self._chart_container = QWidget()
        self._chart_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lay.addWidget(self._chart_container, stretch=1)
        self._chart_layout = QVBoxLayout(self._chart_container)
        self._chart_layout.setContentsMargins(0, 0, 0, 0)
        self._chart_layout.setSpacing(0)
        self._canvas: Optional[FigureCanvas] = None
        self._placeholder = QLabel("No data")
        self._placeholder.setAlignment(Qt.AlignCenter)
        self._placeholder.setStyleSheet("color:#64748b;")
        self.set_summary(None)

    def set_summary(self, summary: Optional[ChartsGridSummary]) -> None:
        while self._chart_layout.count():
            w = self._chart_layout.takeAt(0).widget()
            if w:
                w.deleteLater()
        self._canvas = None
        if summary is None:
            self._chart_layout.addWidget(self._placeholder)
            return

        # Prepare data
        bins = summary.histogram.labels
        flow = summary.histogram.flowrate
        temp = summary.histogram.temperature
        n = min(len(bins), len(flow), len(temp))
        bins = bins[:n]
        flow = flow[:n]
        temp = temp[:n]

        # Create matplotlib figure
        fig = Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)

        # Plot histogram bars side by side (like matplotlib's bar chart)
        import numpy as np
        x = np.arange(len(bins))
        width = 0.35

        bars_flow = ax.bar(x - width/2, flow, width, label='Flowrate', color='#2563eb', alpha=0.6)
        bars_temp = ax.bar(x + width/2, temp, width, label='Temperature', color='#dc2626', alpha=0.6)

        # Correct label collision: rotate and align labels, adjust bottom margin
        ax.set_xticks(x)
        ax.set_xticklabels(bins, rotation=30, ha='right')
        fig.subplots_adjust(bottom=0.22)

        ax.set_xlabel("Categories")
        ax.set_ylabel("Values")
        ax.legend(loc='upper right')
        ax.set_title("Parameter Distribution")

        fig.tight_layout()

        # Add tooltips to bars (corrected: show tooltip only when mouse is over a bar, and clear otherwise)
        def format_tooltip(label, value):
            return f"{label}: {value:.2f}"

        def on_motion(event):
            if event.inaxes != ax:
                self._canvas.setToolTip("")
                return
            tooltip_text = ""
            # Check flowrate bars
            for rect, label, value in zip(bars_flow, bins, flow):
                contains, _ = rect.contains(event)
                if contains:
                    tooltip_text = format_tooltip(f"Flowrate ({label})", value)
                    break
            # Check temperature bars if not found
            if not tooltip_text:
                for rect, label, value in zip(bars_temp, bins, temp):
                    contains, _ = rect.contains(event)
                    if contains:
                        tooltip_text = format_tooltip(f"Temperature ({label})", value)
                        break
            self._canvas.setToolTip(tooltip_text)

        self._canvas = FigureCanvas(fig)
        self._canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._canvas.mpl_connect("motion_notify_event", on_motion)
        self._chart_layout.addWidget(self._canvas, stretch=1)
