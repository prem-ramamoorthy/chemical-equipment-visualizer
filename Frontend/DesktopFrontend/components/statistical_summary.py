from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Union
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QSizePolicy, QGraphicsDropShadowEffect
)

@dataclass
class StatColumn:
    count: int
    mean: float
    std: float
    min: float
    q1: float
    median: float
    q3: float
    max: float

@dataclass
class StatisticalSummaryData:
    flowrate: StatColumn
    pressure: StatColumn
    temperature: StatColumn

def format_value(value: Union[float, int, str]) -> str:
    if isinstance(value, (int, float)):
        if isinstance(value, int) or float(value).is_integer():
            return str(int(value))
        return f"{float(value):.2f}"
    s = str(value)
    import re
    m = re.match(r"^(-?\d+(\.\d+)?)(.*)$", s)
    if m:
        num = float(m.group(1))
        suffix = m.group(3) or ""
        rounded = str(int(num)) if float(num).is_integer() else f"{num:.2f}"
        return f"{rounded}{suffix}"
    return s

def make_card_frame(shadow_alpha: int = 18) -> QFrame:
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
    shadow.setBlurRadius(14)
    shadow.setOffset(0, 4)
    shadow.setColor(QColor(15, 23, 42, shadow_alpha))
    card.setGraphicsEffect(shadow)
    return card

def h2_label(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(12)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#0f172a;")
    return lbl

def subtitle_label(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(9)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#64748b;")
    return lbl

def metric_title(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(11)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#0f172a;")
    return lbl

def icon_box(icon_text: str) -> QFrame:
    box = QFrame()
    box.setFixedSize(32, 32)
    box.setStyleSheet("""
        QFrame {
            background: #eff6ff;
            border-radius: 8px;
        }
    """)
    lay = QVBoxLayout(box)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setAlignment(Qt.AlignCenter)
    lbl = QLabel(icon_text)
    f = QFont()
    f.setPointSize(12)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#2563eb;")
    lay.addWidget(lbl)
    return box

def stat_tile(label: str, value: Union[int, float, str]) -> QFrame:
    tile = QFrame()
    tile.setStyleSheet("""
        QFrame {
            background: #f8fafc;
            border-radius: 8px;
        }
        QLabel#Label {
            color: #64748b;
        }
        QLabel#Value {
            color: #0f172a;
        }
    """)
    lay = QVBoxLayout(tile)
    lay.setContentsMargins(12, 10, 12, 10)
    lay.setSpacing(4)
    l1 = QLabel(label.upper())
    l1.setObjectName("Label")
    f1 = QFont()
    f1.setPointSize(8)
    f1.setBold(False)
    l1.setFont(f1)
    l2 = QLabel(str(value))
    l2.setObjectName("Value")
    f2 = QFont()
    f2.setPointSize(9)
    f2.setBold(True)
    l2.setFont(f2)
    lay.addWidget(l1)
    lay.addWidget(l2)
    return tile

class MetricCardWidget(QWidget):
    def __init__(self, title: str, icon_glyph: str, unit: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._title = title
        self._icon_glyph = icon_glyph
        self._unit = unit
        self.card = make_card_frame(shadow_alpha=18)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self.card)
        self.lay = QVBoxLayout(self.card)
        self.lay.setContentsMargins(16, 16, 16, 16)
        self.lay.setSpacing(12)
        header = QHBoxLayout()
        header.setSpacing(10)
        header.addWidget(icon_box(icon_glyph))
        header.addWidget(metric_title(title))
        header.addStretch(1)
        self.lay.addLayout(header)
        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(12)
        self.grid.setVerticalSpacing(12)
        self.lay.addLayout(self.grid)
        self._tiles = []

    def set_stats(self, stats: StatColumn):
        while self.grid.count():
            it = self.grid.takeAt(0)
            w = it.widget()
            if w:
                w.deleteLater()
        self._tiles.clear()
        items = [
            ("Count", stats.count),
            ("Mean", format_value(f"{stats.mean}{self._unit}")),
            ("Std Dev", format_value(stats.std)),
            ("Min", format_value(f"{stats.min}{self._unit}")),
            ("Q1 (25%)", format_value(f"{stats.q1}{self._unit}")),
            ("Median", format_value(f"{stats.median}{self._unit}")),
            ("Q3 (75%)", format_value(f"{stats.q3}{self._unit}")),
            ("Max", format_value(f"{stats.max}{self._unit}")),
        ]
        for idx, (lab, val) in enumerate(items):
            r = idx // 2
            c = idx % 2
            tile = stat_tile(lab, val)
            self.grid.addWidget(tile, r, c)
            self._tiles.append(tile)

class StatisticalSummarySkeleton(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        card = make_card_frame(shadow_alpha=18)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(14)
        msg = QLabel("Please upload data to view the statistical summary.")
        msg.setAlignment(Qt.AlignCenter)
        msg.setStyleSheet("color:#64748b;")
        msg.setMinimumHeight(60)
        lay.addWidget(msg)
        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)
        lay.addLayout(grid)
        for i in range(3):
            sk = QFrame()
            sk.setStyleSheet("""
                QFrame {
                    background: #f1f5f9;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                }
            """)
            sk.setMinimumHeight(288)
            inner = QVBoxLayout(sk)
            inner.setContentsMargins(16, 16, 16, 16)
            inner.setSpacing(12)
            header = QHBoxLayout()
            badge = QFrame()
            badge.setFixedSize(32, 32)
            badge.setStyleSheet("background:#dbeafe; border-radius:8px;")
            header.addWidget(badge)
            title = QFrame()
            title.setFixedHeight(18)
            title.setFixedWidth(110)
            title.setStyleSheet("background:#e2e8f0; border-radius:6px;")
            header.addWidget(title)
            header.addStretch(1)
            inner.addLayout(header)
            tiles = QGridLayout()
            tiles.setHorizontalSpacing(12)
            tiles.setVerticalSpacing(12)
            for t in range(8):
                tile = QFrame()
                tile.setStyleSheet("background:#e2e8f0; border-radius:8px;")
                tile.setMinimumHeight(56)
                tiles.addWidget(tile, t // 2, t % 2)
            inner.addLayout(tiles)
            grid.addWidget(sk, 0, i)

class StatisticalSummaryWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._data: Optional[StatisticalSummaryData] = None
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(0, 0, 0, 0)
        self.root.setSpacing(16)
        self._header_wrap = QWidget()
        hl = QVBoxLayout(self._header_wrap)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(4)
        hl.addWidget(h2_label("Statistical Summary"))
        hl.addWidget(subtitle_label("Descriptive statistics across operational parameters"))
        self.cards_wrap = QWidget()
        grid = QGridLayout(self.cards_wrap)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(24)
        self.flow_card = MetricCardWidget("Flowrate", "💧", " m³/h")
        self.press_card = MetricCardWidget("Pressure", "🧭", " bar")
        self.temp_card = MetricCardWidget("Temperature", "🔥", " °C")
        grid.addWidget(self.flow_card, 0, 0)
        grid.addWidget(self.press_card, 0, 1)
        grid.addWidget(self.temp_card, 0, 2)
        self._skeleton = StatisticalSummarySkeleton()
        self.set_data(None)

    def set_data(self, data: Optional[StatisticalSummaryData]) -> None:
        while self.root.count():
            it = self.root.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
        self._data = data
        if data is None:
            self.root.addWidget(self._skeleton)
            return
        self.flow_card.set_stats(data.flowrate)
        self.press_card.set_stats(data.pressure)
        self.temp_card.set_stats(data.temperature)
        self.root.addWidget(self._header_wrap)
        self.root.addWidget(self.cards_wrap)
