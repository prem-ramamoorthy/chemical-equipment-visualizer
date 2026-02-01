from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QFrame, QHBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from datetime import datetime


class HistoryList(QWidget):
    dataset_selected = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._current_dataset_id = None
        self._history = []
        self._datasets = {}

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(14)

        header = QLabel("Upload History")
        header.setFont(QFont("Inter", 11, QFont.Bold))
        header.setStyleSheet("color: #0f172a;")

        card_layout.addWidget(header)

        # Empty state widget
        self.empty_widget = QWidget()
        empty_layout = QVBoxLayout(self.empty_widget)
        empty_layout.setAlignment(Qt.AlignCenter)
        
        empty_icon = QLabel("🕒")
        empty_icon.setFont(QFont("Inter", 24))
        empty_icon.setAlignment(Qt.AlignCenter)
        empty_icon.setStyleSheet("color: #94a3b8; opacity: 0.4;")
        
        empty_text = QLabel("No uploads yet")
        empty_text.setFont(QFont("Inter", 9))
        empty_text.setAlignment(Qt.AlignCenter)
        empty_text.setStyleSheet("color: #64748b;")
        
        empty_layout.addWidget(empty_icon)
        empty_layout.addWidget(empty_text)

        self.list_widget = QListWidget()
        self.list_widget.setSpacing(6)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: none;
                outline: none;
            }
            QListWidget::item {
                background: #f8fafc;
                border-radius: 8px;
                padding: 10px;
            }
            QListWidget::item:hover {
                background: #f1f5f9;
            }
            QListWidget::item:selected {
                background: #eff6ff;
                border: 1px solid #93c5fd;
            }
        """)

        self.list_widget.itemClicked.connect(self._on_item_clicked)

        card_layout.addWidget(self.empty_widget)
        card_layout.addWidget(self.list_widget)
        outer_layout.addWidget(card)

        self._update_visibility()

    def _format_date(self, date) -> str:
        """Format date similar to the React component."""
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return date

        if not isinstance(date, datetime):
            return str(date) if date else "Unknown date"

        today = datetime.now()
        is_today = (
            date.date() == today.date()
        )

        if is_today:
            return f"Today, {date.strftime('%I:%M %p')}"

        return date.strftime("%b %d, %I:%M %p")

    def _on_item_clicked(self, item: QListWidgetItem):
        """Handle item click and emit dataset_selected signal."""
        data = item.data(Qt.UserRole)
        if data:
            dataset_id = data.get('dataset_id') or data.get('datasetId') or data.get('id')
            if dataset_id is not None:
                self._current_dataset_id = dataset_id
                self.dataset_selected.emit(dataset_id)
                self._refresh_list()

    def _update_visibility(self):
        """Show empty state or list based on history."""
        has_items = self.list_widget.count() > 0
        self.empty_widget.setVisible(not has_items)
        self.list_widget.setVisible(has_items)

    def _refresh_list(self):
        """Refresh the list to update selection styling."""
        self.list_widget.clear()

        for entry in self._history:
            dataset_id = entry.get('dataset_id') or entry.get('datasetId') or entry.get('id')
            dataset = self._datasets.get(dataset_id, {})

            item = QListWidgetItem()
            filename = entry.get('filename', entry.get('name', 'Unknown'))
            uploaded_at = entry.get('uploaded_at') or entry.get('uploadedAt') or entry.get('date')
            formatted_date = self._format_date(uploaded_at)
            
            count = dataset.get('total_count') or dataset.get('count') or entry.get('count', 0)
            
            item.setText(f"{filename}\n🕒 {formatted_date} • {count} items")
            item.setTextAlignment(Qt.AlignVCenter)
            item.setFont(QFont("Inter", 9))
            item.setData(Qt.UserRole, entry)

            self.list_widget.addItem(item)

            if dataset_id == self._current_dataset_id:
                item.setSelected(True)

        self._update_visibility()

    def set_history(self, history: list, datasets: dict):
        """Update the history list with the provided data.
        
        Args:
            history: List of upload history entries
            datasets: Dict mapping dataset_id to dataset summary
        """
        self._history = history or []
        self._datasets = datasets or {}
        self._refresh_list()

    def set_current_dataset_id(self, dataset_id: int):
        """Set the currently selected dataset ID."""
        self._current_dataset_id = dataset_id
        self._refresh_list()

    def get_current_dataset_id(self):
        """Get the currently selected dataset ID."""
        return self._current_dataset_id
