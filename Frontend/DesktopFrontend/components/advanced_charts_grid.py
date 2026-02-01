from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QWidget, QFrame, QGridLayout, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QSizePolicy, QScrollArea
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


@dataclass
class GridConfig:
    """Configuration for responsive grid breakpoints and columns."""
    mobile_breakpoint: int = 640
    tablet_breakpoint: int = 1024
    desktop_breakpoint: int = 1440
    mobile_cols: int = 1
    tablet_cols: int = 2
    desktop_cols: int = 2
    large_cols: int = 4
    gap: int = 24
    min_card_height: int = 320
    max_card_height: int = 480


def make_skeleton_block(min_height: int = 288) -> QFrame:
    """Create a skeleton loading placeholder block."""
    w = QFrame()
    w.setObjectName("Skeleton")
    w.setMinimumHeight(min_height)
    w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    w.setStyleSheet("""
        QFrame#Skeleton {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #f1f5f9, stop:0.5 #e2e8f0, stop:1 #f1f5f9
            );
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


def make_chart_container(widget: QWidget) -> QFrame:
    """Wrap a chart widget in a styled container with shadow."""
    container = QFrame()
    container.setObjectName("ChartContainer")
    container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    container.setStyleSheet("""
        QFrame#ChartContainer {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
        }
        QFrame#ChartContainer:hover {
            border: 1px solid #cbd5e1;
        }
    """)
    
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setOffset(0, 4)
    shadow.setColor(QColor(15, 23, 42, 30))
    container.setGraphicsEffect(shadow)
    
    layout = QVBoxLayout(container)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.addWidget(widget)
    
    return container


class ResponsiveGrid(QWidget):
    """A responsive grid layout that adapts to container width."""
    
    def __init__(
        self,
        config: Optional[GridConfig] = None,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self.config = config or GridConfig()
        self._items: List[QWidget] = []
        self._current_cols = 2
        
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(self.config.gap)
        self.grid.setVerticalSpacing(self.config.gap)
        
        # Set stretch factors for equal column widths
        for i in range(self.config.large_cols):
            self.grid.setColumnStretch(i, 1)

    def set_items(self, widgets: List[QWidget]) -> None:
        """Set the widgets to display in the grid."""
        # Clear existing items
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        
        self._items = widgets[:]
        self._relayout()

    def add_item(self, widget: QWidget) -> None:
        """Add a single widget to the grid."""
        self._items.append(widget)
        self._relayout()

    def remove_item(self, widget: QWidget) -> None:
        """Remove a widget from the grid."""
        if widget in self._items:
            self._items.remove(widget)
            widget.setParent(None)
            self._relayout()

    def clear(self) -> None:
        """Remove all items from the grid."""
        self.set_items([])

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._relayout()

    def _calculate_columns(self) -> int:
        """Calculate the number of columns based on current width."""
        width = self.width()
        cfg = self.config
        
        if width < cfg.mobile_breakpoint:
            return cfg.mobile_cols
        elif width < cfg.tablet_breakpoint:
            return cfg.tablet_cols
        elif width < cfg.desktop_breakpoint:
            return cfg.desktop_cols
        else:
            return cfg.large_cols

    def _relayout(self) -> None:
        """Recalculate and apply grid layout."""
        cols = self._calculate_columns()
        
        # Only relayout if columns changed or items were modified
        if cols == self._current_cols and self.grid.count() == len(self._items):
            return
        
        self._current_cols = cols
        
        # Clear current layout
        while self.grid.count():
            item = self.grid.takeAt(0)
            # Don't delete widgets, just remove from layout
        
        # Reset column stretches
        for i in range(self.config.large_cols):
            self.grid.setColumnStretch(i, 1 if i < cols else 0)
        
        # Add items to grid
        for idx, widget in enumerate(self._items):
            row = idx // cols
            col = idx % cols
            self.grid.addWidget(widget, row, col)
            
            # Set size constraints
            widget.setMinimumHeight(self.config.min_card_height)
            if self.config.max_card_height:
                widget.setMaximumHeight(self.config.max_card_height)

    def get_column_count(self) -> int:
        """Return the current number of columns."""
        return self._current_cols

    def get_row_count(self) -> int:
        """Return the current number of rows."""
        if not self._items:
            return 0
        return (len(self._items) + self._current_cols - 1) // self._current_cols


class ScrollableGrid(QScrollArea):
    """A scrollable container for the responsive grid."""
    
    def __init__(
        self,
        config: Optional[GridConfig] = None,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 8px;
                border-radius: 4px;
                margin: 4px 2px;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 4px;
                min-height: 40px;
            }
            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)
        
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        self.grid = ResponsiveGrid(config)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 8, 0)  # Right margin for scrollbar
        layout.addWidget(self.grid)
        layout.addStretch()
        
        self.setWidget(container)

    def set_items(self, widgets: List[QWidget]) -> None:
        self.grid.set_items(widgets)


class AdvancedChartsGridWidget(QWidget):
    """Main widget for displaying advanced charts in a responsive grid."""
    
    def __init__(
        self,
        scrollable: bool = False,
        config: Optional[GridConfig] = None,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._config = config or GridConfig()
        
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        
        if scrollable:
            self._grid_container = ScrollableGrid(self._config)
            self.grid = self._grid_container.grid
        else:
            self.grid = ResponsiveGrid(config=self._config)
            self._grid_container = self.grid
        
        outer.addWidget(self._grid_container)
        
        # Create chart widgets
        self.scatter = ScatterChartWidget()
        self.hist = HistogramChartWidget()
        self.box = BoxPlotCard()
        self.heat = CorrelationHeatmapWidget()
        
        # Wrap charts in styled containers
        self._chart_containers = [
            make_chart_container(self.scatter),
            make_chart_container(self.hist),
            make_chart_container(self.box),
            make_chart_container(self.heat),
        ]
        
        # Create skeleton placeholders
        self._skeletons = [
            make_skeleton_block(self._config.min_card_height) 
            for _ in range(4)
        ]
        
        # Initialize with default data
        self.set_summary(self._default_summary())

    def _default_summary(self) -> ChartsGridSummary:
        """Create a default summary with sample data."""
        return ChartsGridSummary(
            scatter_points=[{"x": 1, "y": 2}, {"x": 2, "y": 3}],
            histogram=_HistogramData([1, 2, 3], [4, 5, 6], [300, 310, 320]),
            boxplot=BoxPlotData(
                labels=["A", "B"], 
                values=[[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]]
            ),
            correlation=[
                CorrelationDatum("A", "B", 0.8), 
                CorrelationDatum("B", "C", 0.5)
            ]
        )

    def set_summary(self, summary: Optional[ChartsGridSummary]) -> None:
        """Update all charts with the provided summary data."""
        if summary is None:
            self.grid.set_items(self._skeletons)
            return
        
        # Update individual charts
        self.scatter.set_summary(
            type("S", (), {"scatter_points": summary.scatter_points})()
        )
        self.hist.set_summary(
            type("H", (), {"histogram": summary.histogram})()
        )
        self.box.set_data(summary.boxplot.labels, summary.boxplot.values)
        self.heat.set_data(summary.correlation or [])
        
        # Display chart containers
        self.grid.set_items(self._chart_containers)

    def set_loading(self, loading: bool = True) -> None:
        """Show or hide loading skeletons."""
        if loading:
            self.grid.set_items(self._skeletons)
        else:
            self.grid.set_items(self._chart_containers)

    def get_grid_info(self) -> Dict[str, int]:
        """Return current grid layout information."""
        return {
            "columns": self.grid.get_column_count(),
            "rows": self.grid.get_row_count(),
            "total_items": len(self._chart_containers),
        }

    def set_config(self, config: GridConfig) -> None:
        """Update grid configuration."""
        self._config = config
        self.grid.config = config
        self.grid._relayout()
