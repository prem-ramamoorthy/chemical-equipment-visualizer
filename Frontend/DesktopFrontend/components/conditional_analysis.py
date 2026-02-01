from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QSizePolicy, QGraphicsDropShadowEffect
)

@dataclass
class ConditionalStats:
    flowrate: float
    pressure: float
    temperature: float

@dataclass
class ConditionalAnalysisData:
    conditionLabel: str
    totalRecords: int
    stats: ConditionalStats

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

def h3(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(11)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#0f172a;")
    return lbl

def p_sm(text: str, color: str = "#64748b") -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(9)
    lbl.setFont(f)
    lbl.setStyleSheet(f"color:{color};")
    lbl.setWordWrap(True)
    return lbl

def section_title(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(9)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#334155;")
    return lbl

def badge_box(glyph: str, bg_hex: str, fg_hex: str) -> QFrame:
    box = QFrame()
    box.setFixedSize(32, 32)
    box.setStyleSheet(f"""
        QFrame {{
            background: {bg_hex};
            border-radius: 8px;
        }}
    """)
    lay = QVBoxLayout(box)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setAlignment(Qt.AlignCenter)

    lbl = QLabel(glyph)
    f = QFont()
    f.setPointSize(12)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet(f"color:{fg_hex};")
    lay.addWidget(lbl)
    return box

def metric_row(icon_glyph: str, label: str, value: float, unit: str) -> QFrame:
    row = QFrame()
    row.setStyleSheet("""
        QFrame {
            background: #f8fafc;
            border-radius: 10px;
        }
    """)
    lay = QHBoxLayout(row)
    lay.setContentsMargins(14, 10, 14, 10)
    lay.setSpacing(10)

    left = QHBoxLayout()
    left.setSpacing(10)

    icon = QLabel(icon_glyph)
    fi = QFont()
    fi.setPointSize(10)
    fi.setBold(True)
    icon.setFont(fi)
    icon.setStyleSheet("color:#2563eb;")
    left.addWidget(icon)

    lab = QLabel(label)
    fl = QFont()
    fl.setPointSize(9)
    fl.setBold(True)
    lab.setFont(fl)
    lab.setStyleSheet("color:#334155;")
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

def stat_card_emerald(title: str, big_value: str) -> QFrame:
    card = QFrame()
    card.setStyleSheet("""
        QFrame {
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            border-radius: 10px;
        }
    """)
    lay = QVBoxLayout(card)
    lay.setContentsMargins(14, 10, 14, 10)
    lay.setSpacing(6)

    t = QLabel(title)
    ft = QFont()
    ft.setPointSize(8)
    ft.setBold(True)
    t.setFont(ft)
    t.setStyleSheet("color:#047857;")
    t.setText(t.text().upper())
    lay.addWidget(t)

    row = QHBoxLayout()
    row.setSpacing(8)

    icon = QLabel("↗")
    fi = QFont()
    fi.setPointSize(10)
    fi.setBold(True)
    icon.setFont(fi)
    icon.setStyleSheet("color:#059669;")
    row.addWidget(icon)

    v = QLabel(big_value)
    fv = QFont()
    fv.setPointSize(14)
    fv.setBold(True)
    v.setFont(fv)
    v.setStyleSheet("color:#047857;")
    row.addWidget(v)

    row.addStretch(1)
    lay.addLayout(row)

    return card

def stat_card_slate(title: str, text: str) -> QFrame:
    card = QFrame()
    card.setStyleSheet("""
        QFrame {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
        }
    """)
    lay = QVBoxLayout(card)
    lay.setContentsMargins(14, 10, 14, 10)
    lay.setSpacing(6)

    t = QLabel(title)
    ft = QFont()
    ft.setPointSize(8)
    ft.setBold(True)
    t.setFont(ft)
    t.setStyleSheet("color:#64748b;")
    t.setText(t.text().upper())
    lay.addWidget(t)

    p = QLabel(text)
    fp = QFont()
    fp.setPointSize(9)
    fp.setBold(True)
    p.setFont(fp)
    p.setStyleSheet("color:#334155;")
    p.setWordWrap(True)
    lay.addWidget(p)

    return card

class ConditionalAnalysisSkeleton(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        card = make_card_frame()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(card)

        lay = QVBoxLayout(card)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(16)

        header = QHBoxLayout()
        header.setSpacing(10)

        badge = QFrame()
        badge.setFixedSize(32, 32)
        badge.setStyleSheet("background:#d1fae5; border-radius:8px;")
        header.addWidget(badge)

        col = QVBoxLayout()
        l1 = QFrame()
        l1.setFixedHeight(14)
        l1.setFixedWidth(220)
        l1.setStyleSheet("background:#e2e8f0; border-radius:6px;")
        l2 = QFrame()
        l2.setFixedHeight(12)
        l2.setFixedWidth(140)
        l2.setStyleSheet("background:#e2e8f0; border-radius:6px;")
        col.addWidget(l1)
        col.addWidget(l2)
        header.addLayout(col)
        header.addStretch(1)

        lay.addLayout(header)

class ConditionalAnalysisWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(0, 0, 0, 0)

        self._skeleton = ConditionalAnalysisSkeleton()
        self._card = make_card_frame()
        self._build_ui()

        self.set_data(None)

    def _build_ui(self):
        lay = QVBoxLayout(self._card)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(16)

        header = QHBoxLayout()
        header.setSpacing(10)

        header.addWidget(badge_box("⎇", "#ecfdf5", "#059669"))

        text = QVBoxLayout()
        text.setSpacing(3)
        text.addWidget(h3("Conditional Analysis"))
        self._condition_lbl = p_sm("", "#64748b")
        text.addWidget(self._condition_lbl)
        header.addLayout(text)
        header.addStretch(1)

        lay.addLayout(header)

        top_grid = QGridLayout()
        top_grid.setHorizontalSpacing(16)
        top_grid.setVerticalSpacing(16)

        self._records_card = stat_card_emerald("Records Matching Condition", "0")
        self._summary_card = stat_card_slate("Condition Summary", "Pressure above dataset mean")

        top_grid.addWidget(self._records_card, 0, 0)
        top_grid.addWidget(self._summary_card, 0, 1)

        lay.addLayout(top_grid)

        lay.addWidget(section_title("Average Parameters Under Condition"))

        self._rows_wrap = QWidget()
        rows = QVBoxLayout(self._rows_wrap)
        rows.setContentsMargins(0, 0, 0, 0)
        rows.setSpacing(10)

        self._row_flow = metric_row("〰", "Flowrate", 0.0, " m³/h")
        self._row_pres = metric_row("⎍", "Pressure", 0.0, " bar")
        self._row_temp = metric_row("🌡", "Temperature", 0.0, " °C")

        rows.addWidget(self._row_flow)
        rows.addWidget(self._row_pres)
        rows.addWidget(self._row_temp)

        lay.addWidget(self._rows_wrap)

    def set_data(self, data: Optional[ConditionalAnalysisData]) -> None:
        while self.root.count():
            it = self.root.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)

        if (
            data is None
            or not data.conditionLabel
            or not data.totalRecords
            or data.stats is None
        ):
            self.root.addWidget(self._skeleton)
            return

        self._condition_lbl.setText(data.conditionLabel)

        card_layout = self._card.layout()
        top_grid = card_layout.itemAt(1).layout()

        old_rec = top_grid.itemAtPosition(0, 0).widget()
        if old_rec:
            old_rec.setParent(None)
        self._records_card = stat_card_emerald("Records Matching Condition", str(data.totalRecords))
        top_grid.addWidget(self._records_card, 0, 0)

        old_sum = top_grid.itemAtPosition(0, 1).widget()
        if old_sum:
            old_sum.setParent(None)
        self._summary_card = stat_card_slate("Condition Summary", "Pressure above dataset mean")
        top_grid.addWidget(self._summary_card, 0, 1)

        rows_layout = self._rows_wrap.layout()
        while rows_layout.count():
            w = rows_layout.takeAt(0).widget()
            if w:
                w.setParent(None)

        rows_layout.addWidget(metric_row("〰", "Flowrate", float(data.stats.flowrate), " m³/h"))
        rows_layout.addWidget(metric_row("⎍", "Pressure", float(data.stats.pressure), " bar"))
        rows_layout.addWidget(metric_row("🌡", "Temperature", float(data.stats.temperature), " °C"))

        self.root.addWidget(self._card)
