from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGraphicsDropShadowEffect
)

@dataclass
class MetricStats:
    mean: float
    std: float
    min: float
    max: float

@dataclass
class EquipmentAnalytics:
    flowrate: MetricStats
    pressure: MetricStats
    temperature: MetricStats

GroupedAnalyticsData = Dict[str, EquipmentAnalytics]

def round2(v: float) -> str:
    return f"{float(v):.2f}"

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
    shadow.setBlurRadius(14)
    shadow.setOffset(0, 4)
    shadow.setColor(QColor(15, 23, 42, 18))
    card.setGraphicsEffect(shadow)
    return card

def h2(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(12)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#0f172a;")
    lbl.setWordWrap(True)
    return lbl

def p_sm(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(9)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#64748b;")
    lbl.setWordWrap(True)
    return lbl

def equipment_title(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(11)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#0f172a;")
    return lbl

def icon_badge(glyph: str = "⚙") -> QFrame:
    badge = QFrame()
    badge.setFixedSize(32, 32)
    badge.setStyleSheet("""
        QFrame {
            background: #eff6ff;
            border-radius: 8px;
        }
    """)
    lay = QVBoxLayout(badge)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setAlignment(Qt.AlignCenter)
    lbl = QLabel(glyph)
    f = QFont()
    f.setPointSize(12)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#2563eb;")
    lay.addWidget(lbl)
    return badge

def metric_block(title: str, glyph: str, unit: str, stats: MetricStats) -> QFrame:
    block = QFrame()
    block.setStyleSheet("""
        QFrame {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
        }
    """)
    lay = QVBoxLayout(block)
    lay.setContentsMargins(14, 12, 14, 12)
    lay.setSpacing(10)
    header = QHBoxLayout()
    header.setSpacing(8)
    icon = QLabel(glyph)
    fi = QFont()
    fi.setPointSize(10)
    fi.setBold(True)
    icon.setFont(fi)
    icon.setStyleSheet("color:#2563eb;")
    header.addWidget(icon)
    t = QLabel(title)
    ft = QFont()
    ft.setPointSize(9)
    ft.setBold(True)
    t.setFont(ft)
    t.setStyleSheet("color:#1f2937;")
    header.addWidget(t)
    header.addStretch(1)
    lay.addLayout(header)
    grid = QGridLayout()
    grid.setContentsMargins(0, 0, 0, 0)
    grid.setHorizontalSpacing(16)
    grid.setVerticalSpacing(8)
    def stat_cell(label: str, value: str) -> QWidget:
        w = QWidget()
        vl = QVBoxLayout(w)
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(2)
        l = QLabel(label)
        fl = QFont()
        fl.setPointSize(8)
        l.setFont(fl)
        l.setStyleSheet("color:#64748b;")
        v = QLabel(value)
        fv = QFont()
        fv.setPointSize(9)
        fv.setBold(True)
        v.setFont(fv)
        v.setStyleSheet("color:#0f172a;")
        vl.addWidget(l)
        vl.addWidget(v)
        return w
    grid.addWidget(stat_cell("Mean", f"{round2(stats.mean)}{unit}"), 0, 0)
    grid.addWidget(stat_cell("Std",  f"{round2(stats.std)}"),        0, 1)
    grid.addWidget(stat_cell("Min",  f"{round2(stats.min)}{unit}"),  1, 0)
    grid.addWidget(stat_cell("Max",  f"{round2(stats.max)}{unit}"),  1, 1)
    lay.addLayout(grid)
    return block

class EquipmentAnalyticsCard(QWidget):
    def __init__(self, name: str, analytics: EquipmentAnalytics, parent: Optional[QWidget] = None):
        super().__init__(parent)
        card = make_card_frame()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(14)
        header = QHBoxLayout()
        header.setSpacing(10)
        header.addWidget(icon_badge("🛠"))  # Equipment/Tool
        header.addWidget(equipment_title(name))
        header.addStretch(1)
        lay.addLayout(header)
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)
        grid.addWidget(metric_block("Flowrate", "💧", " m³/h", analytics.flowrate), 0, 0)      # Water drop
        grid.addWidget(metric_block("Pressure", "🔵", " bar", analytics.pressure), 0, 1)       # Blue circle
        grid.addWidget(metric_block("Temperature", "🔥", " °C", analytics.temperature), 0, 2)  # Fire
        lay.addLayout(grid)

class GroupedAnalyticsSkeleton(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)
        head = QWidget()
        hl = QVBoxLayout(head)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(8)
        l1 = QFrame()
        l1.setFixedHeight(18)
        l1.setFixedWidth(260)
        l1.setStyleSheet("background:#e2e8f0; border-radius:8px;")
        l2 = QFrame()
        l2.setFixedHeight(14)
        l2.setFixedWidth(180)
        l2.setStyleSheet("background:#f1f5f9; border-radius:8px;")
        hl.addWidget(l1)
        hl.addWidget(l2)
        root.addWidget(head)
        for _ in range(2):
            sk = make_card_frame()
            sl = QVBoxLayout(sk)
            sl.setContentsMargins(16, 16, 16, 16)
            sl.setSpacing(14)
            top = QHBoxLayout()
            b = QFrame()
            b.setFixedSize(32, 32)
            b.setStyleSheet("background:#e2e8f0; border-radius:8px;")
            top.addWidget(b)
            t = QFrame()
            t.setFixedHeight(16)
            t.setFixedWidth(160)
            t.setStyleSheet("background:#e2e8f0; border-radius:6px;")
            top.addWidget(t)
            top.addStretch(1)
            sl.addLayout(top)
            g = QGridLayout()
            g.setHorizontalSpacing(16)
            g.setVerticalSpacing(16)
            for j in range(3):
                blk = QFrame()
                blk.setStyleSheet("""
                    QFrame {
                        background:#f8fafc;
                        border:1px solid #e2e8f0;
                        border-radius:10px;
                    }
                """)
                blk.setMinimumHeight(120)
                bl = QVBoxLayout(blk)
                bl.setContentsMargins(14, 12, 14, 12)
                bl.setSpacing(10)
                hr = QHBoxLayout()
                ic = QFrame()
                ic.setFixedSize(16, 16)
                ic.setStyleSheet("background:#e2e8f0; border-radius:4px;")
                hr.addWidget(ic)
                tx = QFrame()
                tx.setFixedHeight(12)
                tx.setFixedWidth(90)
                tx.setStyleSheet("background:#e2e8f0; border-radius:6px;")
                hr.addWidget(tx)
                hr.addStretch(1)
                bl.addLayout(hr)
                for _k in range(4):
                    ln = QFrame()
                    ln.setFixedHeight(12)
                    ln.setStyleSheet("background:#e2e8f0; border-radius:6px;")
                    bl.addWidget(ln)
                g.addWidget(blk, 0, j)
            sl.addLayout(g)
            root.addWidget(sk)

class GroupedEquipmentAnalyticsWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(0, 0, 0, 0)
        self.root.setSpacing(16)
        self._skeleton = GroupedAnalyticsSkeleton()
        self._header = QWidget()
        hl = QVBoxLayout(self._header)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(4)
        hl.addWidget(h2("Grouped Analytics by Equipment Type"))
        hl.addWidget(p_sm("Mean, variability, and operating ranges across equipment categories"))
        self._list_wrap = QWidget()
        self._list = QVBoxLayout(self._list_wrap)
        self._list.setContentsMargins(0, 0, 0, 0)
        self._list.setSpacing(16)
        self.set_data(None)
    def set_data(self, data: Optional[GroupedAnalyticsData]) -> None:
        while self.root.count():
            it = self.root.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
        if not data:
            self.root.addWidget(self._skeleton)
            return
        while self._list.count():
            it = self._list.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
        for equipment, analytics in data.items():
            self._list.addWidget(EquipmentAnalyticsCard(equipment, analytics))
        self.root.addWidget(self._header)
        self.root.addWidget(self._list_wrap)
