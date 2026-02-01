from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea
from PyQt5.QtCore import Qt

from components.navbar import Navbar
from components.file_upload import FileUpload
from components.summary_cards import SummaryCards
from components.charts import Charts
from components.data_table import DataTable
from components.history_list import HistoryList

from components.advanced_charts_grid import (
    AdvancedChartsGridWidget,
    ChartsGridSummary,
    BoxPlotData,
)

from components.histogram_chart import HistogramData
from components.correlation_heatmap import CorrelationDatum
from api.client import logout_user


class DashboardPage(QWidget):
    def __init__(self, app, username="Guest"):
        super().__init__()
        self.app = app
        self.setObjectName("Dashboard")
        self.username = username
        self.init_ui()

        self.load_advanced_from_mock()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget#Dashboard {
                background-color: #f8fafc; /* slate-50 */
            }

            QFrame#Container {
                background: transparent;
            }

            QFrame#Card {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.navbar = Navbar(self.username, self.logout)
        root.addWidget(self.navbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        scroll.setWidget(scroll_content)

        scroll_layout = QHBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)

        container = QFrame()
        container.setObjectName("Container")
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(24, 32, 24, 32)
        container_layout.setSpacing(24)

        sidebar = QVBoxLayout()
        sidebar.setSpacing(24)
        sidebar.setAlignment(Qt.AlignTop)

        self.upload = FileUpload(self.on_upload)
        self.history = HistoryList(self.on_select)

        self.wrap_card(self.upload, sidebar)
        self.wrap_card(self.history, sidebar)

        main = QVBoxLayout()
        main.setSpacing(24)
        main.setAlignment(Qt.AlignTop)

        self.summary = SummaryCards()
        self.charts = Charts()
        self.table = DataTable()

        self.advanced = AdvancedChartsGridWidget()

        self.wrap_card(self.summary, main)
        self.wrap_card(self.charts, main)

        self.wrap_card(self.advanced, main)

        self.wrap_card(self.table, main)

        container_layout.addLayout(sidebar, 1)
        container_layout.addLayout(main, 3)

        wrapper = QHBoxLayout()
        wrapper.addStretch()
        wrapper.addWidget(container)
        wrapper.addStretch()

        scroll_layout.addLayout(wrapper)

        root.addWidget(scroll)

    def wrap_card(self, widget, layout):
        """Wrap components in card-style containers"""
        card = QFrame()
        card.setObjectName("Card")

        v = QVBoxLayout(card)
        v.setContentsMargins(16, 16, 16, 16)
        v.addWidget(widget)

        layout.addWidget(card)

    def load_advanced_from_mock(self):
        raw = [
            {"Equipment Name":"Reactor-1","Type":"Reactor","Flowrate":"133.4","Pressure":"7.0","Temperature":"135.6"},
            {"Equipment Name":"HeatExchanger-1","Type":"HeatExchanger","Flowrate":"157.5","Pressure":"6.4","Temperature":"142.6"},
            {"Equipment Name":"Condenser-1","Type":"Condenser","Flowrate":"158.9","Pressure":"7.2","Temperature":"134.0"},
            {"Equipment Name":"Pump-1","Type":"Pump","Flowrate":"115.1","Pressure":"5.0","Temperature":"106.4"},
            {"Equipment Name":"Pump-2","Type":"Pump","Flowrate":"116.5","Pressure":"5.2","Temperature":"109.8"},
            {"Equipment Name":"Condenser-2","Type":"Condenser","Flowrate":"165.7","Pressure":"7.4","Temperature":"125.2"},
            {"Equipment Name":"Condenser-3","Type":"Condenser","Flowrate":"160.8","Pressure":"7.4","Temperature":"125.4"},
            {"Equipment Name":"Valve-1","Type":"Valve","Flowrate":"62.7","Pressure":"4.2","Temperature":"112.7"},
            {"Equipment Name":"Pump-3","Type":"Pump","Flowrate":"134.3","Pressure":"5.9","Temperature":"114.0"},
            {"Equipment Name":"HeatExchanger-2","Type":"HeatExchanger","Flowrate":"140.8","Pressure":"5.9","Temperature":"123.2"},
            {"Equipment Name":"Condenser-4","Type":"Condenser","Flowrate":"173.8","Pressure":"7.0","Temperature":"131.3"},
            {"Equipment Name":"Compressor-1","Type":"Compressor","Flowrate":"89.3","Pressure":"8.5","Temperature":"104.8"},
            {"Equipment Name":"Valve-2","Type":"Valve","Flowrate":"51.3","Pressure":"3.5","Temperature":"109.4"},
            {"Equipment Name":"Pump-4","Type":"Pump","Flowrate":"130.5","Pressure":"5.4","Temperature":"118.7"},
            {"Equipment Name":"HeatExchanger-3","Type":"HeatExchanger","Flowrate":"140.2","Pressure":"6.9","Temperature":"127.8"},
            {"Equipment Name":"Reactor-2","Type":"Reactor","Flowrate":"144.3","Pressure":"6.8","Temperature":"135.8"},
            {"Equipment Name":"Reactor-3","Type":"Reactor","Flowrate":"130.0","Pressure":"7.3","Temperature":"137.6"},
            {"Equipment Name":"Valve-3","Type":"Valve","Flowrate":"52.0","Pressure":"4.2","Temperature":"102.7"},
            {"Equipment Name":"Condenser-5","Type":"Condenser","Flowrate":"156.3","Pressure":"6.8","Temperature":"122.3"},
            {"Equipment Name":"HeatExchanger-4","Type":"HeatExchanger","Flowrate":"153.2","Pressure":"6.7","Temperature":"134.1"},
            {"Equipment Name":"HeatExchanger-5","Type":"HeatExchanger","Flowrate":"158.6","Pressure":"5.8","Temperature":"143.1"},
            {"Equipment Name":"Valve-4","Type":"Valve","Flowrate":"61.8","Pressure":"3.9","Temperature":"105.7"},
            {"Equipment Name":"Pump-5","Type":"Pump","Flowrate":"123.5","Pressure":"5.2","Temperature":"107.9"},
            {"Equipment Name":"Condenser-6","Type":"Condenser","Flowrate":"172.9","Pressure":"6.6","Temperature":"128.9"},
            {"Equipment Name":"HeatExchanger-6","Type":"HeatExchanger","Flowrate":"159.9","Pressure":"6.1","Temperature":"130.6"},
            {"Equipment Name":"Condenser-7","Type":"Condenser","Flowrate":"160.9","Pressure":"7.3","Temperature":"131.2"},
            {"Equipment Name":"Condenser-8","Type":"Condenser","Flowrate":"169.9","Pressure":"7.2","Temperature":"130.2"},
        ]

        summary = self.build_charts_grid_summary(raw)
        self.advanced.set_summary(summary)

    def build_charts_grid_summary(self, records):
        flow = []
        pres = []
        temp = []
        types = []

        for r in records:
            try:
                flow.append(float(r["Flowrate"]))
                pres.append(float(r["Pressure"]))
                temp.append(float(r["Temperature"]))
                types.append(str(r["Type"]))
            except Exception:
                continue

        scatter_points = [{"x": x, "y": y} for x, y in zip(flow, pres)]

        bins, flow_counts = self._hist_counts(flow, bins_count=10)
        _, temp_counts = self._hist_counts(temp, bins_count=10, bin_edges=bins)

        bin_labels = [f"{bins[i]:.0f}-{bins[i+1]:.0f}" for i in range(len(bins) - 1)]
        histogram = HistogramData(labels=bin_labels, flowrate=flow_counts, temperature=temp_counts)

        box_labels, box_values = self._boxplot_by_type(types, pres)

        boxplot = BoxPlotData(labels=box_labels, values=box_values)

        corr = self._correlation_matrix(flow, pres, temp)

        return ChartsGridSummary(
            scatter_points=scatter_points,
            histogram=histogram,
            boxplot=boxplot,
            correlation=corr,
        )

    def _hist_counts(self, values, bins_count=10, bin_edges=None):
        if not values:
            edges = [0.0, 1.0]
            return edges, [0]

        vmin = min(values)
        vmax = max(values)
        if vmax == vmin:
            vmax = vmin + 1.0

        if bin_edges is None:
            step = (vmax - vmin) / bins_count
            edges = [vmin + i * step for i in range(bins_count + 1)]
        else:
            edges = bin_edges

        counts = [0 for _ in range(len(edges) - 1)]
        for v in values:
            idx = len(edges) - 2
            for i in range(len(edges) - 1):
                if edges[i] <= v < edges[i + 1]:
                    idx = i
                    break
            counts[idx] += 1

        return edges, counts

    def _percentile(self, sorted_vals, p):
        if not sorted_vals:
            return 0.0
        n = len(sorted_vals)
        if n == 1:
            return float(sorted_vals[0])
        k = (n - 1) * (p / 100.0)
        f = int(k)
        c = min(f + 1, n - 1)
        if f == c:
            return float(sorted_vals[f])
        d0 = sorted_vals[f] * (c - k)
        d1 = sorted_vals[c] * (k - f)
        return float(d0 + d1)

    def _boxplot_by_type(self, types, pressures):
        groups = {}
        for t, p in zip(types, pressures):
            groups.setdefault(t, []).append(p)

        labels = sorted(groups.keys())
        values = []
        for t in labels:
            arr = sorted(groups[t])
            vmin = float(arr[0])
            q1 = self._percentile(arr, 25)
            med = self._percentile(arr, 50)
            q3 = self._percentile(arr, 75)
            vmax = float(arr[-1])
            values.append([vmin, q1, med, q3, vmax])

        return labels, values

    def _pearson(self, a, b):
        n = min(len(a), len(b))
        if n < 2:
            return 0.0
        a = a[:n]
        b = b[:n]
        ma = sum(a) / n
        mb = sum(b) / n
        num = 0.0
        da = 0.0
        db = 0.0
        for i in range(n):
            xa = a[i] - ma
            xb = b[i] - mb
            num += xa * xb
            da += xa * xa
            db += xb * xb
        if da == 0.0 or db == 0.0:
            return 0.0
        return num / ((da ** 0.5) * (db ** 0.5))

    def _correlation_matrix(self, flow, pres, temp):
        labels = ["Flowrate", "Pressure", "Temperature"]
        series = {
            "Flowrate": flow,
            "Pressure": pres,
            "Temperature": temp,
        }

        out = []
        for x in labels:
            for y in labels:
                v = 1.0 if x == y else self._pearson(series[x], series[y])
                out.append(CorrelationDatum(x=x, y=y, v=float(v)))
        return out

    def on_upload(self, filename):
        dataset = filename
        self.summary.update(dataset)
        self.charts.update(dataset)
        self.table.update(dataset)

        self.load_advanced_from_mock()

    def on_select(self, dataset):
        self.summary.update(dataset)
        self.charts.update(dataset)
        self.table.update(dataset)

        self.load_advanced_from_mock()

    def logout(self):
        logout_user()
        self.app.show_login()
