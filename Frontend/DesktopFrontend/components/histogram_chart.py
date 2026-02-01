from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPainter
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QSizePolicy
)

QTCHARTS_AVAILABLE = True
try:
    from PyQt5.QtChart import (
        QChart, QChartView, QBarSeries, QBarSet,
        QBarCategoryAxis, QValueAxis
    )
except Exception:
    QTCHARTS_AVAILABLE = False

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
        self._chart_view: Optional[QChartView] = None
        self._placeholder = QLabel("No data")
        self._placeholder.setAlignment(Qt.AlignCenter)
        self._placeholder.setStyleSheet("color:#64748b;")
        self._no_qtcharts = QLabel("QtCharts not available.\nInstall PyQtChart.")
        self._no_qtcharts.setAlignment(Qt.AlignCenter)
        self._no_qtcharts.setStyleSheet("color:#64748b;")
        self.set_summary(None)

    def set_summary(self, summary: Optional[ChartsGridSummary]) -> None:
        while self._chart_layout.count():
            w = self._chart_layout.takeAt(0).widget()
            if w:
                w.deleteLater()
        self._chart_view = None
        if summary is None:
            self._chart_layout.addWidget(self._placeholder)
            return
        if not QTCHARTS_AVAILABLE:
            self._chart_layout.addWidget(self._no_qtcharts)
            return
        bins = summary.histogram.labels
        flow = summary.histogram.flowrate
        temp = summary.histogram.temperature
        n = min(len(bins), len(flow), len(temp))
        bins = bins[:n]
        flow = flow[:n]
        temp = temp[:n]
        flow_set = QBarSet("Flowrate")
        temp_set = QBarSet("Temperature")
        for v in flow:
            flow_set.append(float(v))
        for v in temp:
            temp_set.append(float(v))
        flow_set.setColor(QColor(37, 99, 235, 153))
        temp_set.setColor(QColor(220, 38, 38, 153))
        series = QBarSeries()
        series.append(flow_set)
        series.append(temp_set)
        chart = QChart()
        chart.addSeries(series)
        chart.setBackgroundVisible(False)
        chart.setTitle("Flowrate vs Temperature Distribution")
        tfont = QFont()
        tfont.setPointSize(12)
        tfont.setBold(True)
        chart.setTitleFont(tfont)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignTop)
        axis_x = QBarCategoryAxis()
        axis_x.append([str(b) for b in bins])
        axis_x.setTitleText("Value")
        axis_y = QValueAxis()
        axis_y.setTitleText("Frequency")
        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
        self._chart_view = QChartView(chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)
        self._chart_view.setStyleSheet("background: transparent;")
        self._chart_layout.addWidget(self._chart_view, stretch=1)
        if QTCHARTS_AVAILABLE:
            self._chart_view.setMouseTracking(True)
            self._chart_view.viewport().installEventFilter(self)

    def eventFilter(self, obj, event):
        if QTCHARTS_AVAILABLE and self._chart_view and obj == self._chart_view.viewport():
            if event.type() == event.MouseMove:
                # QChart does not have an 'items' method; show a generic tooltip or implement custom logic here
                self._chart_view.setToolTip("Hover over bars to see details.")
        return super().eventFilter(obj, event)
