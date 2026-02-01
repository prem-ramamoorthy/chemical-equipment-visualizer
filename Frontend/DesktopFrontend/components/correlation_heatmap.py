from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Set
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QBrush
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect
)

@dataclass
class CorrelationDatum:
    x: str
    y: str
    v: float

def get_unique_labels(data: List[CorrelationDatum]) -> List[str]:
    labels: Set[str] = set()
    for d in data:
        labels.add(d.x)
        labels.add(d.y)
    return sorted(labels)

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

def heading_label(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(11)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#0f172a;")
    return lbl

class HeatmapCanvas(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._data: List[CorrelationDatum] = []
        self._labels: List[str] = []
        self._map = {}
        self.setMouseTracking(True)
        self._tip = QLabel(self)
        self._tip.setVisible(False)
        self._tip.setStyleSheet("""
            QLabel {
                background: #111827;
                color: white;
                padding: 6px 8px;
                border-radius: 8px;
                font-size: 11px;
            }
        """)
        self._hover_cell = None

    def set_data(self, data: List[CorrelationDatum]) -> None:
        self._data = data or []
        self._labels = get_unique_labels(self._data)
        self._map = {(d.x, d.y): float(d.v) for d in self._data}
        self._hover_cell = None
        self._tip.setVisible(False)
        self.update()

    def _value_for(self, xlab: str, ylab: str) -> Optional[float]:
        if (xlab, ylab) in self._map:
            return self._map[(xlab, ylab)]
        if (ylab, xlab) in self._map:
            return self._map[(ylab, xlab)]
        return None

    def _cell_color(self, v: float) -> QColor:
        a = max(0.0, min(1.0, abs(v)))
        alpha = int(a * 255)
        if v > 0:
            return QColor(33, 150, 243, alpha)
        if v < 0:
            return QColor(244, 67, 54, alpha)
        return QColor(148, 163, 184, 60)

    def _layout_rects(self):
        pad_left = 80
        pad_bottom = 55
        pad_top = 10
        pad_right = 10
        r = self.rect().adjusted(pad_left, pad_top, -pad_right, -pad_bottom)
        return r, pad_left, pad_bottom

    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), QBrush(QColor("#ffffff")))
        if not self._labels:
            p.setPen(QPen(QColor("#94a3b8")))
            p.drawText(self.rect(), Qt.AlignCenter, "No correlation data")
            return
        grid_rect, pad_left, pad_bottom = self._layout_rects()
        n = len(self._labels)
        if n <= 0:
            return
        cell_w = max(6, int(grid_rect.width() / n) - 2)
        cell_h = max(6, int(grid_rect.height() / n) - 2)
        border_pen = QPen(QColor(255, 255, 255, int(0.8 * 255)))
        border_pen.setWidth(1)
        tick_font = QFont()
        tick_font.setPointSize(9)
        p.setFont(tick_font)
        p.setPen(QPen(QColor("#334155")))
        for row, ylab in enumerate(self._labels):
            y = grid_rect.top() + row * (cell_h + 2)
            p.drawText(6, y + cell_h//2 + 4, pad_left - 12, 16, Qt.AlignRight, ylab)
        for col, xlab in enumerate(self._labels):
            x = grid_rect.left() + col * (cell_w + 2)
            p.drawText(x, grid_rect.bottom() + 10, cell_w, 40, Qt.AlignHCenter | Qt.AlignTop, xlab)
        for row, ylab in enumerate(self._labels):
            for col, xlab in enumerate(self._labels):
                v = self._value_for(xlab, ylab)
                if v is None:
                    fill = QColor(226, 232, 240, 120)
                else:
                    fill = self._cell_color(v)
                x = grid_rect.left() + col * (cell_w + 2)
                y = grid_rect.top() + row * (cell_h + 2)
                cell = QRect(x, y, cell_w, cell_h)
                p.fillRect(cell, QBrush(fill))
                p.setPen(border_pen)
                p.drawRect(cell)
                if self._hover_cell == (row, col):
                    hl = QPen(QColor("#0f172a"))
                    hl.setWidth(2)
                    p.setPen(hl)
                    p.drawRect(cell.adjusted(0, 0, -1, -1))

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not self._labels:
            self._tip.setVisible(False)
            self._hover_cell = None
            return
        grid_rect, _, _ = self._layout_rects()
        pos = event.pos()
        if not grid_rect.contains(pos):
            self._tip.setVisible(False)
            self._hover_cell = None
            self.update()
            return
        n = len(self._labels)
        cell_w = max(6, int(grid_rect.width() / n) - 2)
        cell_h = max(6, int(grid_rect.height() / n) - 2)
        step_x = cell_w + 2
        step_y = cell_h + 2
        col = (pos.x() - grid_rect.left()) // step_x
        row = (pos.y() - grid_rect.top()) // step_y
        if row < 0 or col < 0 or row >= n or col >= n:
            self._tip.setVisible(False)
            self._hover_cell = None
            self.update()
            return
        self._hover_cell = (int(row), int(col))
        xlab = self._labels[int(col)]
        ylab = self._labels[int(row)]
        v = self._value_for(xlab, ylab)
        if v is None:
            self._tip.setVisible(False)
            self.update()
            return
        self._tip.setText(f"Correlation: {v:.2f}")
        self._tip.adjustSize()
        tip_w = self._tip.width()
        tip_h = self._tip.height()
        x = pos.x() + 12
        y = pos.y() - tip_h - 12
        if x + tip_w > self.width():
            x = self.width() - tip_w - 8
        if y < 0:
            y = pos.y() + 12
        self._tip.move(QPoint(x, y))
        self._tip.setVisible(True)
        self.update()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self._tip.setVisible(False)
        self._hover_cell = None
        self.update()

    def mousePressEvent(self, event):
        # Disable cell selection/highlighting
        super().mousePressEvent(event)
        # No selection logic

class CorrelationHeatmapWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._card = make_card_frame()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self._card)
        lay = QVBoxLayout(self._card)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)
        lay.addWidget(heading_label("Correlation Heatmap"))
        self.canvas = HeatmapCanvas()
        self.canvas.setMinimumHeight(320)
        lay.addWidget(self.canvas)

    def set_data(self, data: List[CorrelationDatum]) -> None:
        self.canvas.set_data(data)
