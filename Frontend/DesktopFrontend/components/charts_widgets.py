from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QBrush
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGraphicsDropShadowEffect, QSizePolicy, QPushButton, QInputDialog
)

QTCHARTS_AVAILABLE = True
try:
    from PyQt5.QtChart import (
        QChart, QChartView, QPieSeries, QBarSeries, QBarSet,
        QBarCategoryAxis, QValueAxis
    )
except Exception:
    QTCHARTS_AVAILABLE = False

@dataclass
class DatasetSummary:
    type_distribution: Dict[str, int]
    avg_flowrate: float
    avg_pressure: float
    avg_temperature: float

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

def icon_badge(text: str = "●") -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(12)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color: #2563eb;")
    lbl.setFixedWidth(16)
    lbl.setAlignment(Qt.AlignCenter)
    return lbl

class SkeletonCard(QFrame):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        card = make_card_frame()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)
        bar = QFrame()
        bar.setFixedHeight(12)
        bar.setFixedWidth(128)
        bar.setStyleSheet("background:#e2e8f0; border-radius:6px;")
        lay.addWidget(bar, alignment=Qt.AlignLeft)
        area = QFrame()
        area.setMinimumHeight(256)
        area.setStyleSheet("background:#e2e8f0; border-radius:10px;")
        lay.addWidget(area)

class PieChartCard(QWidget):
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
        header.addWidget(icon_badge("◔"))
        header.addWidget(title_label("Equipment Type Distribution"))
        header.addStretch(1)
        lay.addLayout(header)
        self._chart_container = QWidget()
        self._chart_container.setMinimumHeight(256)
        lay.addWidget(self._chart_container)
        self._chart_layout = QVBoxLayout(self._chart_container)
        self._chart_layout.setContentsMargins(0, 0, 0, 0)
        self._chart_view: Optional[QChartView] = None
        self._fallback = QLabel("QtCharts not available.\nInstall PyQtChart.")
        self._fallback.setAlignment(Qt.AlignCenter)
        self._fallback.setStyleSheet("color:#64748b;")
        self.interactive_btn = QPushButton("Edit Distribution")
        self.interactive_btn.clicked.connect(self.edit_distribution)
        lay.addWidget(self.interactive_btn)
        self._data = {}

    def set_data(self, type_distribution: Dict[str, int]) -> None:
        self._data = type_distribution.copy()
        while self._chart_layout.count():
            w = self._chart_layout.takeAt(0).widget()
            if w:
                w.deleteLater()
        if not QTCHARTS_AVAILABLE:
            self._chart_layout.addWidget(self._fallback)
            return
        series = QPieSeries()
        for k, v in type_distribution.items():
            series.append(str(k), float(v))
        colors = [
            QColor("#2f6aa3"),
            QColor("#2e8a8f"),
            QColor("#f59e0b"),
            QColor("#a855f7"),
            QColor("#22c55e"),
        ]
        for i, s in enumerate(series.slices()):
            s.setBrush(QBrush(colors[i % len(colors)]))
            s.setPen(QPen(Qt.NoPen))
        chart = QChart()
        chart.addSeries(series)
        chart.setBackgroundVisible(False)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        self._chart_view = QChartView(chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)
        self._chart_view.setStyleSheet("background: transparent;")
        self._chart_layout.addWidget(self._chart_view)

    def edit_distribution(self):
        items = list(self._data.keys())
        if not items:
            return
        item, ok = QInputDialog.getItem(self, "Edit Type", "Select type:", items, 0, False)
        if ok and item:
            value, ok2 = QInputDialog.getInt(self, "Edit Value", f"Set value for {item}:", self._data[item], 0, 10000)
            if ok2:
                self._data[item] = value
                self.set_data(self._data)

class BarChartCard(QWidget):
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
        header.addWidget(title_label("Average Parameters"))
        header.addStretch(1)
        lay.addLayout(header)
        self._chart_container = QWidget()
        self._chart_container.setMinimumHeight(256)
        lay.addWidget(self._chart_container)
        self._chart_layout = QVBoxLayout(self._chart_container)
        self._chart_layout.setContentsMargins(0, 0, 0, 0)
        self._chart_view: Optional[QChartView] = None
        self._fallback = QLabel("QtCharts not available.\nInstall PyQtChart.")
        self._fallback.setAlignment(Qt.AlignCenter)
        self._fallback.setStyleSheet("color:#64748b;")
        self.interactive_btn = QPushButton("Edit Parameters")
        self.interactive_btn.clicked.connect(self.edit_parameters)
        lay.addWidget(self.interactive_btn)
        self._values = [0.0, 0.0, 0.0]

    def set_data(self, avg_flowrate: float, avg_pressure: float, avg_temperature: float) -> None:
        self._values = [avg_flowrate, avg_pressure, avg_temperature]
        while self._chart_layout.count():
            w = self._chart_layout.takeAt(0).widget()
            if w:
                w.deleteLater()
        if not QTCHARTS_AVAILABLE:
            self._chart_layout.addWidget(self._fallback)
            return
        categories = ["Flowrate (m³/h)", "Pressure (bar)", "Temperature (°C)"]
        values = [avg_flowrate, avg_pressure, avg_temperature]
        barset = QBarSet("Average Values")
        for v in values:
            barset.append(float(v))
        barset.setColor(QColor("#0ea5e9"))
        series = QBarSeries()
        series.append(barset)
        chart = QChart()
        chart.addSeries(series)
        chart.setBackgroundVisible(False)
        chart.legend().setVisible(False)
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        axis_y = QValueAxis()
        axis_y.setGridLineColor(QColor("#d8dee9"))
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        self._chart_view = QChartView(chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)
        self._chart_view.setStyleSheet("background: transparent;")
        self._chart_layout.addWidget(self._chart_view)

    def edit_parameters(self):
        labels = ["Flowrate (m³/h)", "Pressure (bar)", "Temperature (°C)"]
        for i, label in enumerate(labels):
            value, ok = QInputDialog.getDouble(self, "Edit Parameter", f"Set value for {label}:", self._values[i], 0, 10000, 2)
            if ok:
                self._values[i] = value
        self.set_data(*self._values)

class BoxPlotCanvas(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.labels: List[str] = []
        self.values: List[List[float]] = []
        self.setMinimumHeight(288)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._tooltip_text = ""
        self._tooltip_rect = QRect()
        self.setMouseTracking(True)

    def set_boxplot(self, labels: List[str], values: List[List[float]]) -> None:
        self.labels = labels
        self.values = values
        self.update()

    def mouseMoveEvent(self, event):
        self._tooltip_text = ""
        self._tooltip_rect = QRect()
        
        rect = self.rect().adjusted(16, 10, -16, -24)
        if not self.labels or not self.values:
            self.update()
            return
        
        all_vals = [v for row in self.values for v in row if len(row) >= 5]
        if not all_vals:
            self.update()
            return
            
        gmin = min(all_vals)
        gmax = max(all_vals)
        if gmax == gmin:
            gmax += 1.0
        
        left = rect.left() + 32
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()
        
        n = len(self.labels)
        slot_w = (right - left) / max(1, n)
        box_w = max(18, int(slot_w * 0.45))
        
        def y_map(v: float) -> int:
            return int(top + (gmax - v) * (bottom - top) / (gmax - gmin))
        
        for i, (lab, row) in enumerate(zip(self.labels, self.values)):
            if len(row) < 5:
                continue
            vmin, q1, med, q3, vmax = row[:5]
            cx = left + slot_w * (i + 0.5)
            
            y_q1 = y_map(q1)
            y_q3 = y_map(q3)
            x0 = int(cx - box_w / 2)
            
            box_rect = QRect(x0, y_q3, box_w, max(2, y_q1 - y_q3))
            
            if box_rect.contains(event.pos()):
                self._tooltip_text = f"\n{lab}\nMin: {vmin:.2f}\nQ1: {q1:.2f}\nMedian: {med:.2f}\nQ3: {q3:.2f}\nMax: {vmax:.2f}"
                self._tooltip_rect = box_rect
                self.update()
                return
        
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(16, 10, -16, -24)
        if not self.labels or not self.values:
            p.setPen(QPen(QColor("#94a3b8")))
            p.drawText(rect, Qt.AlignCenter, "No boxplot data")
            return
        all_vals = [v for row in self.values for v in row if len(row) >= 5]
        gmin = min(all_vals)
        gmax = max(all_vals)
        if gmax == gmin:
            gmax += 1.0
        left = rect.left() + 32
        right = rect.right()
        top = rect.top()
        bottom = rect.bottom()
        grid_pen = QPen(QColor("#d8dee9"))
        grid_pen.setWidth(1)
        p.setPen(grid_pen)
        for t in range(6):
            y = top + int((bottom - top) * t / 5)
            p.drawLine(left, y, right, y)
        tick_pen = QPen(QColor("#475569"))
        p.setPen(tick_pen)
        font = QFont()
        font.setPointSize(9)
        p.setFont(font)
        for t in range(6):
            val = gmax - (gmax - gmin) * t / 5
            y = top + int((bottom - top) * t / 5)
            p.drawText(rect.left(), y + 4, 40, 14, Qt.AlignLeft, f"{val:.1f}")
        n = len(self.labels)
        if n == 0:
            return
        slot_w = (right - left) / max(1, n)
        box_w = max(18, int(slot_w * 0.45))
        box_brush = QBrush(QColor("#3b82f6"))
        box_pen = QPen(QColor("#334155"))
        box_pen.setWidth(2)
        whisker_pen = QPen(QColor("#334155"))
        whisker_pen.setWidth(2)
        def y_map(v: float) -> int:
            return int(top + (gmax - v) * (bottom - top) / (gmax - gmin))
        for i, (lab, row) in enumerate(zip(self.labels, self.values)):
            if len(row) < 5:
                continue
            vmin, q1, med, q3, vmax = row[:5]
            cx = left + slot_w * (i + 0.5)
            y_min = y_map(vmin)
            y_q1 = y_map(q1)
            y_med = y_map(med)
            y_q3 = y_map(q3)
            y_max = y_map(vmax)
            p.setPen(whisker_pen)
            p.drawLine(int(cx), y_max, int(cx), y_min)
            cap = int(box_w * 0.55)
            p.drawLine(int(cx - cap/2), y_max, int(cx + cap/2), y_max)
            p.drawLine(int(cx - cap/2), y_min, int(cx + cap/2), y_min)
            p.setPen(box_pen)
            p.setBrush(box_brush)
            x0 = int(cx - box_w/2)
            p.drawRoundedRect(x0, y_q3, box_w, max(2, y_q1 - y_q3), 6, 6)
            p.setBrush(Qt.NoBrush)
            p.drawLine(x0, y_med, x0 + box_w, y_med)
            p.setPen(QPen(QColor("#475569")))
            p.drawText(int(cx - slot_w/2), bottom + 6, int(slot_w), 16, Qt.AlignCenter, lab)
        
        # Draw tooltip
        if self._tooltip_text:
            tooltip_font = QFont()
            tooltip_font.setPointSize(8)
            p.setFont(tooltip_font)
            
            metrics = p.fontMetrics()
            lines = self._tooltip_text.split('\n')
            max_width = max(metrics.width(line) for line in lines)
            line_height = metrics.height()
            
            tooltip_width = max_width + 12
            tooltip_height = len(lines) * line_height + 8
            
            tooltip_x = min(self._tooltip_rect.right() + 5, self.width() - tooltip_width - 5)
            tooltip_y = max(5, self._tooltip_rect.top())
            
            p.fillRect(tooltip_x, tooltip_y, tooltip_width, tooltip_height, QColor("#1f2937"))
            p.setPen(QPen(QColor("#d1d5db")))
            p.drawRect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
            
            p.setPen(QColor("#f3f4f6"))
            for idx, line in enumerate(lines):
                p.drawText(tooltip_x + 6, tooltip_y + 4 + idx * line_height, line)

class BoxPlotCard(QWidget):
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
        header.addWidget(icon_badge("↕"))
        header.addWidget(title_label("Pressure Distribution by Equipment Type"))
        header.addStretch(1)
        lay.addLayout(header)
        self.canvas = BoxPlotCanvas()
        lay.addWidget(self.canvas)
        self._labels = []
        self._values = []

    def set_data(self, labels: List[str], values: List[List[float]]) -> None:
        self._labels = labels[:]
        self._values = [v[:] for v in values]
        self.canvas.set_boxplot(labels, values)

class ResponsiveGrid(QWidget):
    def __init__(self, gap: int = 16, breakpoint: int = 900, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.gap = gap
        self.breakpoint = breakpoint
        self._items: List[QWidget] = []
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(gap)
        self.grid.setVerticalSpacing(gap)

    def set_items(self, widgets: List[QWidget]) -> None:
        while self.grid.count():
            it = self.grid.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
        self._items = widgets[:]
        self._relayout()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._relayout()

    def _relayout(self) -> None:
        cols = 2 if self.width() >= self.breakpoint else 1
        for idx, w in enumerate(self._items):
            r = idx // cols
            c = idx % cols
            self.grid.addWidget(w, r, c)

class ChartsWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.grid = ResponsiveGrid(gap=16, breakpoint=1024)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self.grid)
        self._pie = PieChartCard()
        self._bar = BarChartCard()
        self._s1 = SkeletonCard()
        self._s2 = SkeletonCard()
        self.set_summary(None)

    def set_summary(self, summary: Optional[DatasetSummary]) -> None:
        if summary is None:
            self.grid.set_items([self._s1, self._s2])
            return
        self._pie.set_data(summary.type_distribution)
        self._bar.set_data(summary.avg_flowrate, summary.avg_pressure, summary.avg_temperature)
        self.grid.set_items([self._pie, self._bar])
