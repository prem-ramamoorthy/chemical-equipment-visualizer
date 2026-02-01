from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGraphicsDropShadowEffect
)

@dataclass
class DistributionStats:
    min: float
    q1: float
    median: float
    q3: float
    max: float
    outliers: Optional[List[float]] = None

@dataclass
class DistributionAnalysisData:
    title: str
    unit: str
    stats: DistributionStats

def round2(v: float) -> float:
    return float(f"{v:.2f}")

def make_card_frame(shadow_md: bool = True) -> QFrame:
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
    shadow.setBlurRadius(18 if shadow_md else 14)
    shadow.setOffset(0, 6 if shadow_md else 4)
    shadow.setColor(QColor(15, 23, 42, 26 if shadow_md else 18))
    card.setGraphicsEffect(shadow)
    return card

def h3(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(11)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#0f172a;")
    lbl.setWordWrap(True)
    return lbl

def p_sm(text: str, color: str = "#64748b") -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(9)
    lbl.setFont(f)
    lbl.setStyleSheet(f"color:{color};")
    lbl.setWordWrap(True)
    return lbl

def stat_card(label: str, value: float, unit: str) -> QFrame:
    card = QFrame()
    card.setStyleSheet("""
        QFrame {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
        }
    """)
    lay = QVBoxLayout(card)
    lay.setContentsMargins(14, 12, 14, 12)
    lay.setSpacing(6)
    l = QLabel(label.upper())
    fl = QFont()
    fl.setPointSize(8)
    fl.setBold(True)
    l.setFont(fl)
    l.setStyleSheet("color:#64748b; letter-spacing: 1px;")
    lay.addWidget(l)
    v = QLabel(f"{round2(value):.2f}{unit}")
    fv = QFont()
    fv.setPointSize(14)
    fv.setBold(True)
    v.setFont(fv)
    v.setStyleSheet("color:#0f172a;")
    lay.addWidget(v)
    return card

def skew_card(skew: str) -> QFrame:
    is_right = (skew == "Right Skewed")
    card = QFrame()
    card.setStyleSheet("""
        QFrame {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
        }
    """)
    lay = QVBoxLayout(card)
    lay.setContentsMargins(14, 12, 14, 12)
    lay.setSpacing(8)
    l = QLabel("DISTRIBUTION")
    fl = QFont()
    fl.setPointSize(8)
    fl.setBold(True)
    l.setFont(fl)
    l.setStyleSheet("color:#64748b; letter-spacing: 1px;")
    lay.addWidget(l)
    row = QHBoxLayout()
    row.setSpacing(8)
    icon = QLabel("↑" if is_right else "↓")
    fi = QFont()
    fi.setPointSize(12)
    fi.setBold(True)
    icon.setFont(fi)
    icon.setStyleSheet("color:#059669;" if is_right else "color:#4f46e5;")
    row.addWidget(icon)
    txt = QLabel(skew)
    ft = QFont()
    ft.setPointSize(9)
    ft.setBold(True)
    txt.setFont(ft)
    txt.setStyleSheet("color:#1f2937;")
    row.addWidget(txt)
    row.addStretch(1)
    lay.addLayout(row)
    return card

def interpretation_box(text_html: str) -> QFrame:
    box = QFrame()
    box.setStyleSheet("""
        QFrame {
            background: #f8fafc;
            border-radius: 10px;
        }
    """)
    lay = QVBoxLayout(box)
    lay.setContentsMargins(16, 14, 16, 14)
    lay.setSpacing(8)
    head = QLabel("Interpretation")
    fh = QFont()
    fh.setPointSize(9)
    fh.setBold(True)
    head.setFont(fh)
    head.setStyleSheet("color:#334155;")
    lay.addWidget(head)
    body = QLabel(text_html)
    body.setTextFormat(Qt.RichText)
    body.setWordWrap(True)
    body.setStyleSheet("color:#475569; font-size:12px;")
    lay.addWidget(body)
    return box

def outlier_notice(count: int) -> QWidget:
    row = QWidget()
    lay = QHBoxLayout(row)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setSpacing(8)
    icon = QLabel("⚠")
    fi = QFont()
    fi.setPointSize(11)
    fi.setBold(True)
    icon.setFont(fi)
    icon.setStyleSheet("color:#d97706;")
    lay.addWidget(icon)
    txt = QLabel(f"{count} potential outlier(s) detected which may require further inspection.")
    txt.setWordWrap(True)
    txt.setStyleSheet("color:#d97706; font-size:12px;")
    lay.addWidget(txt, 1)
    return row

class DistributionAnalysisSkeleton(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        card = make_card_frame(shadow_md=False)
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
        badge.setStyleSheet("background:#dbeafe; border-radius:8px;")
        header.addWidget(badge)
        col = QVBoxLayout()
        l1 = QFrame()
        l1.setFixedHeight(14)
        l1.setFixedWidth(240)
        l1.setStyleSheet("background:#e2e8f0; border-radius:6px;")
        l2 = QFrame()
        l2.setFixedHeight(12)
        l2.setFixedWidth(160)
        l2.setStyleSheet("background:#e2e8f0; border-radius:6px;")
        col.addWidget(l1)
        col.addWidget(l2)
        header.addLayout(col)
        header.addStretch(1)
        lay.addLayout(header)

class DistributionAnalysisWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(0, 0, 0, 0)
        self._skeleton = DistributionAnalysisSkeleton()
        self._card = make_card_frame(shadow_md=True)
        self._build_ui()
        self.set_data(None)

    def _build_ui(self):
        lay = QVBoxLayout(self._card)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(16)
        header = QHBoxLayout()
        header.setSpacing(10)
        icon = QLabel("⟲")
        fi = QFont()
        fi.setPointSize(14)
        fi.setBold(True)
        icon.setFont(fi)
        icon.setStyleSheet("color:#2563eb;")
        header.addWidget(icon)
        text = QVBoxLayout()
        text.setSpacing(3)
        self._title = h3("")
        self._sub = p_sm("Statistical summary based on quartile distribution", "#64748b")
        text.addWidget(self._title)
        text.addWidget(self._sub)
        header.addLayout(text)
        header.addStretch(1)
        lay.addLayout(header)
        self._grid_wrap = QWidget()
        self._grid = QGridLayout(self._grid_wrap)
        self._grid.setContentsMargins(0, 0, 0, 0)
        self._grid.setHorizontalSpacing(16)
        self._grid.setVerticalSpacing(16)
        lay.addWidget(self._grid_wrap)
        self._interp_wrap = QWidget()
        self._interp_lay = QVBoxLayout(self._interp_wrap)
        self._interp_lay.setContentsMargins(0, 0, 0, 0)
        self._interp_lay.setSpacing(8)
        lay.addWidget(self._interp_wrap)

    def set_data(self, data: Optional[DistributionAnalysisData]) -> None:
        while self.root.count():
            it = self.root.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
        if data is None or not data.title or data.stats is None:
            self.root.addWidget(self._skeleton)
            return
        title = data.title
        unit = data.unit or ""
        stats = data.stats
        iqr = round2(stats.q3 - stats.q1)
        rng = round2(stats.max - stats.min)
        skew = "Right Skewed" if (stats.median - stats.q1) > (stats.q3 - stats.median) else "Left Skewed"
        self._title.setText(f"{title} – Distribution Analysis")
        while self._grid.count():
            it = self._grid.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
        self._grid.addWidget(stat_card("Median", stats.median, unit), 0, 0)
        self._grid.addWidget(stat_card("IQR", iqr, unit), 0, 1)
        self._grid.addWidget(stat_card("Range", rng, unit), 0, 2)
        self._grid.addWidget(skew_card(skew), 0, 3)
        while self._interp_lay.count():
            it = self._interp_lay.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
        interp_html = (
            f"The median value of <b>{round2(stats.median):.2f}{unit}</b> indicates "
            f"the central tendency of the dataset. The interquartile range (IQR) "
            f"of <b>{iqr:.2f}{unit}</b> reflects moderate variability, "
            f"while the total range suggests the overall spread. "
            f"The distribution is <b>{skew}</b>, indicating unequal "
            f"dispersion around the median."
        )
        box = interpretation_box(interp_html)
        self._interp_lay.addWidget(box)
        if stats.outliers and len(stats.outliers) > 0:
            self._interp_lay.addWidget(outlier_notice(len(stats.outliers)))
        self.root.addWidget(self._card)
