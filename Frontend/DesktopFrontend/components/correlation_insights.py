from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGraphicsDropShadowEffect, QSizePolicy, QTableWidget, QTableWidgetItem,
    QAbstractItemView
)

CorrelationMatrix = Dict[str, Dict[str, float]]

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

def title_label(text: str) -> QLabel:
    lbl = QLabel(text)
    f = QFont()
    f.setPointSize(11)
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

def badge_icon(glyph: str = "📊") -> QFrame:
    box = QFrame()
    box.setFixedSize(32, 32)
    box.setStyleSheet("""
        QFrame {
            background: #eef2ff;
            border-radius: 8px;
        }
    """)
    lay = QVBoxLayout(box)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.setAlignment(Qt.AlignCenter)
    lbl = QLabel(glyph)
    f = QFont()
    f.setPointSize(12)
    f.setBold(True)
    lbl.setFont(f)
    lbl.setStyleSheet("color:#4f46e5;")
    lay.addWidget(lbl)
    return box

def make_interpretation_box() -> QFrame:
    box = QFrame()
    box.setStyleSheet("""
        QFrame {
            background: #f8fafc;
            border-radius: 10px;
        }
    """)
    return box

def get_strength(value: float) -> Tuple[str, str, str]:
    abs_v = abs(value)
    if abs_v >= 0.7:
        return ("Strong", "⬆️", "color:#059669;")
    if abs_v >= 0.4:
        return ("Moderate", "➖", "color:#d97706;")
    return ("Weak", "⬇️", "color:#64748b;")

class CorrelationInsightsSkeleton(QWidget):
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
        badge = QFrame()
        badge.setFixedSize(32, 32)
        badge.setStyleSheet("background:#e0e7ff; border-radius:8px;")
        header.addWidget(badge)
        text_col = QVBoxLayout()
        line1 = QFrame()
        line1.setFixedHeight(14)
        line1.setFixedWidth(140)
        line1.setStyleSheet("background:#e2e8f0; border-radius:6px;")
        line2 = QFrame()
        line2.setFixedHeight(12)
        line2.setFixedWidth(220)
        line2.setStyleSheet("background:#f1f5f9; border-radius:6px;")
        text_col.addWidget(line1)
        text_col.addWidget(line2)
        header.addLayout(text_col)
        header.addStretch(1)
        lay.addLayout(header)
        table = QFrame()
        table.setStyleSheet("background:transparent;")
        tlay = QVBoxLayout(table)
        tlay.setContentsMargins(0, 0, 0, 0)
        tlay.setSpacing(8)
        row = QHBoxLayout()
        row.addWidget(QFrame())
        for _ in range(3):
            c = QFrame()
            c.setFixedHeight(12)
            c.setFixedWidth(80)
            c.setStyleSheet("background:#e2e8f0; border-radius:6px;")
            row.addWidget(c)
        row.addStretch(1)
        tlay.addLayout(row)
        for _ in range(3):
            body_row = QHBoxLayout()
            rlab = QFrame()
            rlab.setFixedHeight(12)
            rlab.setFixedWidth(80)
            rlab.setStyleSheet("background:#e2e8f0; border-radius:6px;")
            body_row.addWidget(rlab)
            for _ in range(3):
                cell = QFrame()
                cell.setFixedHeight(18)
                cell.setFixedWidth(120)
                cell.setStyleSheet("background:#f1f5f9; border-radius:6px;")
                body_row.addWidget(cell)
            body_row.addStretch(1)
            tlay.addLayout(body_row)
        lay.addWidget(table)
        box = make_interpretation_box()
        blay = QVBoxLayout(box)
        blay.setContentsMargins(16, 14, 16, 14)
        blay.setSpacing(8)
        h = QFrame()
        h.setFixedHeight(12)
        h.setFixedWidth(160)
        h.setStyleSheet("background:#e2e8f0; border-radius:6px;")
        blay.addWidget(h)
        for _ in range(3):
            l = QFrame()
            l.setFixedHeight(12)
            l.setStyleSheet("background:#f1f5f9; border-radius:6px;")
            blay.addWidget(l)
        lay.addWidget(box)

class CorrelationInsightsWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._matrix: Optional[CorrelationMatrix] = None
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(0, 0, 0, 0)
        self._skeleton = CorrelationInsightsSkeleton()
        self._card = make_card_frame()
        self._build_normal_ui()
        self.set_matrix(None)

    def _build_normal_ui(self):
        lay = QVBoxLayout(self._card)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(16)
        header = QHBoxLayout()
        header.setSpacing(10)
        header.addWidget(badge_icon("📊"))
        text = QVBoxLayout()
        text.setSpacing(3)
        text.addWidget(title_label("Correlation Insights"))
        text.addWidget(subtitle_label("Relationship strength between operational parameters"))
        header.addLayout(text)
        header.addStretch(1)
        lay.addLayout(header)
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                background: transparent;
                font-size: 12px;
            }
            QTableWidget::item {
                border-bottom: 1px solid #f1f5f9;
                padding: 10px 12px;
                color: #0f172a;
            }
        """)
        lay.addWidget(self.table)
        self.interp = make_interpretation_box()
        il = QVBoxLayout(self.interp)
        il.setContentsMargins(16, 14, 16, 14)
        il.setSpacing(8)
        il.addWidget(section_title("Interpretation Summary"))
        self.i1 = QLabel("<b>Flowrate &amp; Pressure:</b> Moderate positive correlation (≈ 0.50), indicating pressure generally increases with flowrate.")
        self.i2 = QLabel("<b>Flowrate &amp; Temperature:</b> Strong positive correlation (≈ 0.70), suggesting higher flowrates are associated with higher temperatures.")
        self.i3 = QLabel("<b>Pressure &amp; Temperature:</b> Weak correlation (≈ 0.16), implying largely independent behavior.")
        for w in (self.i1, self.i2, self.i3):
            w.setTextFormat(Qt.RichText)
            w.setWordWrap(True)
            w.setStyleSheet("color:#475569; font-size:12px;")
            il.addWidget(w)
        lay.addWidget(self.interp)

    def set_matrix(self, matrix: Optional[CorrelationMatrix]) -> None:
        while self.root.count():
            it = self.root.takeAt(0)
            w = it.widget()
            if w:
                w.setParent(None)
        self._matrix = matrix
        if not matrix:
            self.root.addWidget(self._skeleton)
            return
        self._populate_table(matrix)
        self.root.addWidget(self._card)

    def _populate_table(self, matrix: CorrelationMatrix) -> None:
        variables = list(matrix.keys())
        rows = 1 + len(variables)
        cols = 1 + len(variables)
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)
        self.table.setItem(0, 0, QTableWidgetItem(""))
        for j, v in enumerate(variables, start=1):
            it = QTableWidgetItem(v)
            it.setForeground(QColor("#334155"))
            f = QFont()
            f.setBold(True)
            it.setFont(f)
            self.table.setItem(0, j, it)
        for i, row_var in enumerate(variables, start=1):
            rlab = QTableWidgetItem(row_var)
            rlab.setForeground(QColor("#334155"))
            f = QFont()
            f.setBold(True)
            rlab.setFont(f)
            self.table.setItem(i, 0, rlab)
            for j, col_var in enumerate(variables, start=1):
                value = float(matrix.get(row_var, {}).get(col_var, 0.0))
                strength_label, icon_glyph, color_css = get_strength(value)
                if row_var == col_var:
                    text = f"{value:.2f}"
                else:
                    text = f"{value:.2f}   {icon_glyph} {strength_label}"
                item = QTableWidgetItem(text)
                item.setForeground(QColor("#0f172a"))
                self.table.setItem(i, j, item)
                if row_var != col_var:
                    if "color:#059669" in color_css:
                        item.setForeground(QColor("#059669"))
                    elif "color:#d97706" in color_css:
                        item.setForeground(QColor("#d97706"))
                    else:
                        item.setForeground(QColor("#64748b"))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        if cols > 0:
            self.table.setColumnWidth(0, max(120, self.table.columnWidth(0)))
        self.table.horizontalHeader().setStretchLastSection(True)
