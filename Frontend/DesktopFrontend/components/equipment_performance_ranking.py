from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QSizePolicy, QGraphicsDropShadowEffect
)

@dataclass
class PerformanceMetrics:
    flowrate: float
    pressure: float
    temperature: float

EquipmentRankingData = Dict[str, PerformanceMetrics]

def make_card_frame(shadow_sm: bool = True) -> QFrame:
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
    shadow.setBlurRadius(14 if shadow_sm else 10)
    shadow.setOffset(0, 4 if shadow_sm else 3)
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

def metric_row(icon_glyph: str, label: str, value: float, unit: str) -> QFrame:
    row = QFrame()
    row.setStyleSheet("""
        QFrame {
            background: #f8fafc;
            border-radius: 10px;
        }
    """)
    lay = QHBoxLayout(row)
    lay.setContentsMargins(14, 8, 14, 8)
    lay.setSpacing(10)

    left = QHBoxLayout()
    left.setSpacing(8)

    icon = QLabel(icon_glyph)
    fi = QFont()
    fi.setPointSize(10)
    fi.setBold(True)
    icon.setFont(fi)
    icon.setStyleSheet("color:#64748b;")
    left.addWidget(icon)

    lab = QLabel(label)
    fl = QFont()
    fl.setPointSize(8)
    fl.setBold(False)
    lab.setFont(fl)
    lab.setStyleSheet("color:#475569;")
    left.addWidget(lab)

    leftw = QWidget()
    leftw.setLayout(left)

    val = QLabel(f"{value:.2f}{unit}")
    fv = QFont()
    fv.setPointSize(9)
    fv.setBold(True)
    val.setFont(fv)
    val.setStyleSheet("color:#0f172a;")
    val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    lay.addWidget(leftw, 1)
    lay.addWidget(val, 0)
    return row

def rank_badge(rank: int) -> QFrame:
    if rank == 1:
        bg, fg, bd = "#fef9c3", "#a16207", "#fcd34d"
    elif rank == 2:
        bg, fg, bd = "#f1f5f9", "#334155", "#cbd5e1"
    elif rank == 3:
        bg, fg, bd = "#ffedd5", "#b45309", "#fdba74"
    else:
        bg, fg, bd = "#f8fafc", "#475569", "#e2e8f0"

    badge = QFrame()
    badge.setFixedSize(36, 36)
    badge.setStyleSheet(f"""
        QFrame {{
            background: {bg};
            border: 1px solid {bd};
            border-radius: 18px;
        }}
    """)
    lay = QVBoxLayout(badge)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setAlignment(Qt.AlignCenter)

    lbl = QLabel(f"#{rank}")
    f = QFont()
    f.setPointSize(9)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet(f"color:{fg};")
    lay.addWidget(lbl)
    return badge

def trophy_tag() -> QWidget:
    w = QWidget()
    lay = QHBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(6)

    icon = QLabel("🏆")
    fi = QFont()
    fi.setPointSize(10)
    fi.setBold(True)
    icon.setFont(fi)
    icon.setStyleSheet("color:#ca8a04;")
    lay.addWidget(icon)

    txt = QLabel("Top Performer")
    ft = QFont()
    ft.setPointSize(8)
    ft.setBold(True)
    txt.setFont(ft)
    txt.setStyleSheet("color:#ca8a04;")
    lay.addWidget(txt)

    return w

class EquipmentCardWidget(QWidget):
    def __init__(self, name: str, rank: int, metrics: PerformanceMetrics, parent: Optional[QWidget] = None):
        super().__init__(parent)

        card = make_card_frame(shadow_sm=True)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)

        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        header = QHBoxLayout()
        header.setSpacing(10)

        left = QHBoxLayout()
        left.setSpacing(10)
        left.addWidget(rank_badge(rank))

        title = QLabel(name)
        ft = QFont()
        ft.setPointSize(11)
        ft.setBold(True)
        title.setFont(ft)
        title.setStyleSheet("color:#0f172a;")
        left.addWidget(title)

        leftw = QWidget()
        leftw.setLayout(left)

        header.addWidget(leftw, 1)

        if rank == 1:
            header.addWidget(trophy_tag(), 0, Qt.AlignRight)

        lay.addLayout(header)

        lay.addWidget(metric_row("💧", "Flowrate", metrics.flowrate, " m³/h"))
        lay.addWidget(metric_row("⏲️", "Pressure", metrics.pressure, " bar"))
        lay.addWidget(metric_row("🌡️", "Temperature", metrics.temperature, " °C"))

        lay.addStretch(1)

class EquipmentRankingSkeleton(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)

        hwrap = QWidget()
        hl = QVBoxLayout(hwrap)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(8)

        l1 = QFrame()
        l1.setFixedHeight(18)
        l1.setFixedWidth(260)
        l1.setStyleSheet("background:#e2e8f0; border-radius:8px;")
        l2 = QFrame()
        l2.setFixedHeight(14)
        l2.setFixedWidth(160)
        l2.setStyleSheet("background:#f1f5f9; border-radius:8px;")

        hl.addWidget(l1)
        hl.addWidget(l2)
        root.addWidget(hwrap)

        grid_wrap = QWidget()
        grid = QGridLayout(grid_wrap)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(24)
        grid.setVerticalSpacing(24)

        for i in range(3):
            sk = make_card_frame(shadow_sm=True)
            sk.setMinimumHeight(240)

            sl = QVBoxLayout(sk)
            sl.setContentsMargins(16, 16, 16, 16)
            sl.setSpacing(12)

            top = QHBoxLayout()
            left = QHBoxLayout()
            left.setSpacing(10)

            b = QFrame()
            b.setFixedSize(36, 36)
            b.setStyleSheet("background:#f1f5f9; border:1px solid #e2e8f0; border-radius:18px;")
            left.addWidget(b)

            nm = QFrame()
            nm.setFixedHeight(16)
            nm.setFixedWidth(110)
            nm.setStyleSheet("background:#e2e8f0; border-radius:6px;")
            left.addWidget(nm)

            lw = QWidget()
            lw.setLayout(left)
            top.addWidget(lw, 1)

            tag = QFrame()
            tag.setFixedHeight(14)
            tag.setFixedWidth(90)
            tag.setStyleSheet("background:#fef9c3; border-radius:6px;")
            top.addWidget(tag, 0, Qt.AlignRight)

            sl.addLayout(top)

            for _ in range(3):
                r = QFrame()
                r.setStyleSheet("background:#f8fafc; border-radius:10px;")
                r.setFixedHeight(34)
                rl = QHBoxLayout(r)
                rl.setContentsMargins(14, 8, 14, 8)

                icon = QFrame()
                icon.setFixedSize(16, 16)
                icon.setStyleSheet("background:#e2e8f0; border-radius:4px;")
                rl.addWidget(icon)

                txt = QFrame()
                txt.setFixedHeight(10)
                txt.setFixedWidth(70)
                txt.setStyleSheet("background:#e2e8f0; border-radius:6px;")
                rl.addWidget(txt)

                rl.addStretch(1)

                val = QFrame()
                val.setFixedHeight(12)
                val.setFixedWidth(55)
                val.setStyleSheet("background:#e2e8f0; border-radius:6px;")
                rl.addWidget(val)

                sl.addWidget(r)

            grid.addWidget(sk, 0, i)

        root.addWidget(grid_wrap)

class EquipmentPerformanceRankingWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(0, 0, 0, 0)
        self.root.setSpacing(16)

        self._skeleton = EquipmentRankingSkeleton()

        self._header_wrap = QWidget()
        hl = QVBoxLayout(self._header_wrap)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(4)
        hl.addWidget(h2("Equipment Performance Ranking"))
        hl.addWidget(p_sm("Ranked by operational performance metrics"))

        self._grid_wrap = QWidget()
        self._grid = QGridLayout(self._grid_wrap)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setHorizontalSpacing(24)
        self._grid.setVerticalSpacing(24)

        self.set_data(None)

    def set_data(self, data: Optional[EquipmentRankingData]) -> None:
        while self.root.count():
            it = self.root.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)

        if not data:
            self.root.addWidget(self._skeleton)
            return

        ranked: List[Tuple[str, PerformanceMetrics]] = sorted(
            data.items(), key=lambda kv: kv[1].flowrate, reverse=True
        )

        while self._grid.count():
            it = self._grid.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)

        cols = 3
        for idx, (name, metrics) in enumerate(ranked):
            r = idx // cols
            c = idx % cols
            card = EquipmentCardWidget(name=name, rank=idx + 1, metrics=metrics)
            self._grid.addWidget(card, r, c)

        self.root.addWidget(self._header_wrap)
        self.root.addWidget(self._grid_wrap)
