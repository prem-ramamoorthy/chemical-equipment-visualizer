from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QWidget, QFrame, QGridLayout, QVBoxLayout,
    QGraphicsDropShadowEffect, QSizePolicy
)

from .scatter_chart import ScatterChartWidget
from .histogram_chart import HistogramChartWidget, HistogramData as _HistogramData
from .correlation_heatmap import CorrelationHeatmapWidget, CorrelationDatum
from .charts_widgets import BoxPlotCard

@dataclass
class BoxPlotData:
    labels: List[str]
    values: List[List[float]]

@dataclass
class ChartsGridSummary:
    scatter_points: List[Dict[str, Any]]
    histogram: _HistogramData
    boxplot: BoxPlotData
    correlation: List[CorrelationDatum]

def make_skeleton_block() -> QFrame:
    w = QFrame()
    w.setObjectName("Skeleton")
    w.setMinimumHeight(288)
    w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    w.setStyleSheet("""
        QFrame#Skeleton {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
        }
    """)
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(18)
    shadow.setOffset(0, 6)
    shadow.setColor(QColor(15, 23, 42, 25))
    w.setGraphicsEffect(shadow)
    return w

class ResponsiveGrid(QWidget):
    def __init__(self, gap: int = 16, breakpoint: int = 1024, parent: Optional[QWidget] = None):
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
        # Always 2 rows and 2 columns if width >= breakpoint (tablet)
        cols = 2 if self.width() >= self.breakpoint else 1
        for idx, w in enumerate(self._items):
            r = idx // cols
            c = idx % cols
            self.grid.addWidget(w, r, c)

class AdvancedChartsGridWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        self.grid = ResponsiveGrid(gap=24, breakpoint=1024)
        outer.addWidget(self.grid)
        self.scatter = ScatterChartWidget()
        self.hist = HistogramChartWidget()
        self.box = BoxPlotCard()
        self.heat = CorrelationHeatmapWidget()
        self._skeletons = [make_skeleton_block() for _ in range(4)]
        self.set_summary(self._default_summary())

    def _default_summary(self) -> ChartsGridSummary:
        return ChartsGridSummary(
            scatter_points=[{"x": 1, "y": 2}, {"x": 2, "y": 3}],
            histogram=_HistogramData([1, 2, 3], [4, 5, 6], [300, 310, 320]),
            boxplot=BoxPlotData(labels=["A", "B"], values=[[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]),
            correlation=[CorrelationDatum("A", "B", 0.8), CorrelationDatum("B", "C", 0.5)]
        )

    def set_summary(self, summary: Optional[ChartsGridSummary]) -> None:
        if summary is None:
            self.grid.set_items(self._skeletons)
            return
        self.scatter.set_summary(type("S", (), {"scatter_points": summary.scatter_points})())
        self.hist.set_summary(type("H", (), {"histogram": summary.histogram})())
        self.box.set_data(summary.boxplot.labels, summary.boxplot.values)
        self.heat.set_data(summary.correlation or [])
        self.grid.set_items([self.scatter, self.hist, self.box, self.heat])
