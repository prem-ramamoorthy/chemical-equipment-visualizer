from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor, QFont, QPainter
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QSizePolicy
)

QTCHARTS_AVAILABLE = True
try:
    from PyQt5.QtChart import QChart, QChartView, QScatterSeries, QValueAxis
except Exception:
    QTCHARTS_AVAILABLE = False

@dataclass
class ScatterPoint:
    x: float
    y: float

@dataclass
class ChartsGridSummary:
    scatter_points: List[Dict[str, Any]]

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

def icon_badge(text: str = "⟐") -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(12)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color: #2563eb;")
    lbl.setFixedWidth(16)
    lbl.setAlignment(Qt.AlignCenter)
    return lbl

class ScatterChartWidget(QWidget):
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
        header.addWidget(icon_badge("⟐"))
        header.addWidget(title_label("Flowrate vs Pressure"))
        header.addStretch(1)
        lay.addLayout(header)
        self._chart_container = QWidget()
        self._chart_container.setMinimumHeight(256)
        self._chart_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lay.addWidget(self._chart_container)
        self._chart_layout = QVBoxLayout(self._chart_container)
        self._chart_layout.setContentsMargins(0, 0, 0, 0)
        self._chart_view: Optional[QChartView] = None
        self._placeholder = QLabel("No data")
        self._placeholder.setAlignment(Qt.AlignCenter)
        self._placeholder.setStyleSheet("color:#64748b;")
        self._no_qtcharts = QLabel("QtCharts not available.\nInstall PyQtChart.")
        self._no_qtcharts.setAlignment(Qt.AlignCenter)
        self._no_qtcharts.setStyleSheet("color:#64748b;")
        self._tooltip = QLabel("", self)
        self._tooltip.setStyleSheet("background: #f1f5f9; color: #0f172a; border: 1px solid #e2e8f0; border-radius: 6px; padding: 4px;")
        self._tooltip.setVisible(False)
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
        points = summary.scatter_points or []
        series = QScatterSeries()
        series.setName("Flowrate vs Pressure")
        series.setMarkerShape(QScatterSeries.MarkerShapeCircle)
        series.setMarkerSize(8)
        series.setColor(QColor("#0ea5e9"))
        xs = []
        ys = []
        for pt in points:
            try:
                x = float(pt.get("x"))
                y = float(pt.get("y"))
                series.append(x, y)
                xs.append(x)
                ys.append(y)
            except Exception:
                continue
        chart = QChart()
        chart.addSeries(series)
        chart.setBackgroundVisible(False)
        chart.legend().setVisible(False)
        axis_x = QValueAxis()
        axis_x.setTitleText("Flowrate")
        axis_y = QValueAxis()
        axis_y.setTitleText("Pressure")
        if xs and ys:
            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)
            xpad = (xmax - xmin) * 0.08 if xmax != xmin else 1.0
            ypad = (ymax - ymin) * 0.08 if ymax != ymin else 1.0
            axis_x.setRange(xmin - xpad, xmax + xpad)
            axis_y.setRange(ymin - ypad, ymax + ypad)
        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
        self._chart_view = QChartView(chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)
        self._chart_view.setStyleSheet("background: transparent;")
        self._chart_layout.addWidget(self._chart_view)
        self._chart_view.setMouseTracking(True)
        self._chart_view.viewport().installEventFilter(self)

        self._scatter_points = [QPointF(float(pt.get("x")), float(pt.get("y"))) for pt in points if "x" in pt and "y" in pt]

    def eventFilter(self, obj, event):
        if self._chart_view is None or not QTCHARTS_AVAILABLE:
            return False
        if event.type() == event.MouseMove:
            pos = event.pos()
            chart = self._chart_view.chart()
            plot_area = chart.plotArea()
            if not plot_area.contains(pos):
                self._tooltip.setVisible(False)
                return False
            mapped = chart.mapToValue(pos)
            closest = None
            min_dist = float("inf")
            for pt in getattr(self, "_scatter_points", []):
                dist = (pt.x() - mapped.x()) ** 2 + (pt.y() - mapped.y()) ** 2
                if dist < min_dist:
                    min_dist = dist
                    closest = pt
            if closest is not None and min_dist < 0.5:
                self._tooltip.setText(f"Flowrate: {closest.x():.2f}\nPressure: {closest.y():.2f}")
                global_pos = self._chart_view.mapToGlobal(pos)
                self._tooltip.move(self.mapFromGlobal(global_pos + QPointF(16, 16).toPoint()))
                self._tooltip.setVisible(True)
            else:
                self._tooltip.setVisible(False)
        elif event.type() == event.Leave:
            self._tooltip.setVisible(False)
        return False
