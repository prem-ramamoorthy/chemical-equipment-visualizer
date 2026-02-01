from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from components.navbar import Navbar
from components.advanced_charts_grid import (
    AdvancedChartsGridWidget,
    ChartsGridSummary,
    BoxPlotData,
)
from components.histogram_chart import HistogramData
from components.correlation_heatmap import CorrelationDatum
from api.client import logout_user

from components.file_upload import FileUpload
from components.history_list import HistoryList

from components.statistical_summary import (
    StatisticalSummaryWidget,
    StatisticalSummaryData,
    StatColumn,
)

from components.correlation_insights import CorrelationInsightsWidget

from components.conditional_analysis import (
    ConditionalAnalysisWidget,
    ConditionalAnalysisData,
    ConditionalStats,
)

from components.distribution_analysis import (
    DistributionAnalysisWidget,
    DistributionAnalysisData,
    DistributionStats,
)

from components.equipment_performance_ranking import (
    EquipmentPerformanceRankingWidget,
    EquipmentRankingData,
    PerformanceMetrics,
)

from components.grouped_equipment_analytics import (
    GroupedEquipmentAnalyticsWidget,
    GroupedAnalyticsData,
    EquipmentAnalytics,
    MetricStats,
)

from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
import os
import requests

class UploadWorker(QThread):
    finished = pyqtSignal(dict, list)
    error = pyqtSignal(str)

    def __init__(self, file_path: str, api_base_url: str):
        super().__init__()
        self.file_path = file_path
        self.api_base_url = api_base_url

    def run(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            rows = [line.strip() for line in text.split('\n') if line.strip()]
            if len(rows) < 2:
                self.error.emit('CSV must have at least a header and one data row.')
                return

            headers = [h.strip() for h in rows[0].split(',')]
            data = []
            for row in rows[1:]:
                values = []
                current = ''
                in_quotes = False
                for i, char in enumerate(row):
                    if char == '"' and (i == 0 or row[i - 1] != '\\'):
                        in_quotes = not in_quotes
                    elif char == ',' and not in_quotes:
                        values.append(current.strip().strip('"'))
                        current = ''
                    else:
                        current += char
                values.append(current.strip().strip('"'))
                record = {headers[idx]: values[idx] if idx < len(values) else '' for idx in range(len(headers))}
                data.append(record)

            response = requests.post(
                f"{self.api_base_url}/datasets/upload/",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            if not response.ok:
                self.error.emit('Failed to upload CSV')
                return

            serverdata = response.json()
            self.finished.emit(serverdata, data)
        except Exception as e:
            self.error.emit(str(e))
class FetchWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, api_base_url: str):
        super().__init__()
        self.api_base_url = api_base_url

    def run(self):
        try:
            response = requests.get(
                f"{self.api_base_url}/datasets/history/",
            )
            if not response.ok:
                self.error.emit('Failed to fetch datasets')
                return
            result = response.json()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
class DashboardPage(QWidget):
    def __init__(self, app, username: str = "Guest"):
        super().__init__()
        self.app = app
        self.setObjectName("Dashboard")
        self.username = username
        self.api_base_url = os.environ.get("API_BASE_URL", "http://localhost:8000/api")

        self.datasets: Dict[int, Dict[str, Any]] = {}
        self.upload_history: List[Dict[str, Any]] = []
        self.current_dataset: Optional[Dict[str, Any]] = None
        self.current_data: List[Dict[str, Any]] = []
        self.is_uploading = False

        self.init_ui()
        self.fetch_initial_datasets()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget#Dashboard {
                background-color: #f8fafc;
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
        scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        scroll_content = QWidget()
        scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll.setWidget(scroll_content)

        scroll_layout = QHBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)

        container = QFrame()
        container.setObjectName("Container")
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(24, 32, 24, 32)
        container_layout.setSpacing(24)

        sidebar = QVBoxLayout()
        sidebar.setSpacing(24)
        sidebar.setAlignment(Qt.AlignTop)

        self.upload = FileUpload(self.on_upload)
        self.history = HistoryList()
        self.history.dataset_selected.connect(self.on_select)

        self.wrap_card(self.upload, sidebar)
        self.wrap_card(self.history, sidebar)

        main = QVBoxLayout()
        main.setSpacing(24)
        main.setAlignment(Qt.AlignTop)

        self.advanced = AdvancedChartsGridWidget()
        self.advanced.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.wrap_card(self.advanced, main, expand=True)

        self.stat_summary = StatisticalSummaryWidget()
        self.wrap_card(self.stat_summary, main)

        self.corr_insights = CorrelationInsightsWidget()
        self.wrap_card(self.corr_insights, main)

        self.conditional_analysis = ConditionalAnalysisWidget()
        self.wrap_card(self.conditional_analysis, main)

        self.distribution_analysis = DistributionAnalysisWidget()
        self.wrap_card(self.distribution_analysis, main)

        self.equipment_ranking = EquipmentPerformanceRankingWidget()
        self.wrap_card(self.equipment_ranking, main)

        self.grouped_analytics = GroupedEquipmentAnalyticsWidget()
        self.wrap_card(self.grouped_analytics, main)

        container_layout.addLayout(sidebar, 1)
        container_layout.addLayout(main, 4)

        scroll_layout.addWidget(container)
        root.addWidget(scroll)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def wrap_card(self, widget: QWidget, layout: QVBoxLayout, expand=False):
        card = QFrame()
        card.setObjectName("Card")
        v = QVBoxLayout(card)
        v.setContentsMargins(16, 16, 16, 16)
        v.addWidget(widget)
        if expand:
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(card, stretch=1 if expand else 0)

    def fetch_initial_datasets(self):
        self.fetch_worker = FetchWorker(self.api_base_url)
        self.fetch_worker.finished.connect(self.on_fetch_finished)
        self.fetch_worker.error.connect(self.on_fetch_error)
        self.fetch_worker.start()

    def on_fetch_finished(self, result: dict):
        datasets_map: Dict[int, Dict[str, Any]] = {}
        upload_history_arr: List[Dict[str, Any]] = []

        if result and isinstance(result.get("order"), list) and isinstance(result.get("datasets"), dict):
            for id_ in result["order"]:
                ds_obj = result["datasets"].get(str(id_))
                if ds_obj:
                    datasets_map[int(id_)] = {
                        "dataset": ds_obj.get("dataset"),
                        "data": ds_obj.get("data", [])
                    }
                    meta = ds_obj.get("meta", {})
                    upload_history_arr.append({
                        "id": int(id_),
                        "filename": meta.get("name", f"dataset_{id_}"),
                        "uploadedAt": datetime.fromisoformat(meta["uploaded_at"]) if meta.get("uploaded_at") else datetime.now(),
                        "datasetId": int(id_),
                    })

        self.datasets = datasets_map
        self.upload_history = upload_history_arr[:5]
        self.history.set_history(self.upload_history, self.datasets)

        if result.get("order") and len(result["order"]) > 0:
            first_id = result["order"][0]
            first = result["datasets"].get(str(first_id))
            if first:
                self.current_dataset = first.get("dataset")
                self.current_data = first.get("data", [])
                self.update_ui_with_data(self.current_dataset, self.current_data)

    def on_fetch_error(self, error: str):
        print(f"Failed to fetch datasets: {error}")

    def on_upload(self, file_path: str, filename: str):
        if self.is_uploading:
            return
        self.is_uploading = True
        self.upload.set_loading(True)

        self.upload_worker = UploadWorker(file_path, self.api_base_url)
        self.upload_worker.finished.connect(lambda serverdata, data: self.on_upload_finished(serverdata, data, filename))
        self.upload_worker.error.connect(self.on_upload_error)
        self.upload_worker.start()

    def on_upload_finished(self, serverdata: dict, data: list, filename: str):
        self.is_uploading = False
        self.upload.set_loading(False)

        dataset_id = serverdata.get("id", int(datetime.now().timestamp() * 1000))
        self.datasets[dataset_id] = {
            "dataset": serverdata,
            "data": data
        }

        history_item = {
            "id": int(datetime.now().timestamp() * 1000),
            "filename": filename,
            "uploadedAt": datetime.now(),
            "datasetId": dataset_id,
        }
        self.upload_history = [history_item] + self.upload_history
        self.upload_history = self.upload_history[:5]
        self.history.set_history(self.upload_history, self.datasets)

        self.current_dataset = serverdata
        self.current_data = data
        self.update_ui_with_data(serverdata, data)

    def on_upload_error(self, error: str):
        self.is_uploading = False
        self.upload.set_loading(False)
        print(f"Upload failed: {error}")

    def on_select(self, dataset_id: int):
        dataset_entry = self.datasets.get(dataset_id)
        if dataset_entry:
            self.current_dataset = dataset_entry["dataset"]
            self.current_data = dataset_entry["data"]
            self.update_ui_with_data(self.current_dataset, self.current_data)

    def update_ui_with_data(self, dataset: Optional[Dict[str, Any]], data: List[Dict[str, Any]]):
        if dataset:
            # If server returns pre-computed summaries
            if "StatisticalSummary" in dataset:
                stat_data = dataset.get("StatisticalSummary", {}).get("data")
                if stat_data:
                    self.stat_summary.set_data(self._parse_statistical_summary(stat_data))
            else:
                stat_summary = self.build_statistical_summary(data)
                self.stat_summary.set_data(stat_summary)

            if "CorrelationInsights" in dataset:
                corr_matrix = dataset.get("CorrelationInsights", {}).get("matrix")
                if corr_matrix:
                    self.corr_insights.set_matrix(corr_matrix)
            else:
                corr_matrix = self._build_correlation_matrix_dict(data)
                self.corr_insights.set_matrix(corr_matrix)

            if "ConditionalAnalysis" in dataset:
                cond = dataset.get("ConditionalAnalysis", {})
                cond_data = ConditionalAnalysisData(
                    conditionLabel=cond.get("conditionLabel", ""),
                    totalRecords=cond.get("totalRecords", 0),
                    stats=ConditionalStats(
                        flowrate=cond.get("stats", {}).get("flowrate", 0),
                        pressure=cond.get("stats", {}).get("pressure", 0),
                        temperature=cond.get("stats", {}).get("temperature", 0),
                    ) if cond.get("stats") else None,
                )
                self.conditional_analysis.set_data(cond_data)
            else:
                cond_data = self._build_conditional_analysis_data(data)
                self.conditional_analysis.set_data(cond_data)

            if "DistributionAnalysis" in dataset:
                dist = dataset.get("DistributionAnalysis", {})
                dist_stats = dist.get("stats", {})
                dist_data = DistributionAnalysisData(
                    title=dist.get("title", ""),
                    unit=dist.get("unit", ""),
                    stats=DistributionStats(
                        min=dist_stats.get("min", 0),
                        q1=dist_stats.get("q1", 0),
                        median=dist_stats.get("median", 0),
                        q3=dist_stats.get("q3", 0),
                        max=dist_stats.get("max", 0),
                        outliers=dist_stats.get("outliers"),
                    ) if dist_stats else None,
                )
                self.distribution_analysis.set_data(dist_data)
            else:
                dist_data = self._build_distribution_analysis_data(data)
                self.distribution_analysis.set_data(dist_data)

            if "EquipmentPerformanceRanking" in dataset:
                ranking = dataset.get("EquipmentPerformanceRanking", {})
                ranking_data = {}
                for name, metrics in ranking.items():
                    ranking_data[name] = PerformanceMetrics(
                        flowrate=metrics.get("flowrate", 0),
                        pressure=metrics.get("pressure", 0),
                        temperature=metrics.get("temperature", 0),
                    )
                self.equipment_ranking.set_data(ranking_data)
            else:
                ranking_data = self._build_equipment_ranking_data(data)
                self.equipment_ranking.set_data(ranking_data)

            if "GroupedEquipmentAnalytics" in dataset:
                grouped = dataset.get("GroupedEquipmentAnalytics", {})
                grouped_data = {}
                for typ, analytics in grouped.items():
                    grouped_data[typ] = EquipmentAnalytics(
                        flowrate=self._parse_metric_stats(analytics.get("flowrate")),
                        pressure=self._parse_metric_stats(analytics.get("pressure")),
                        temperature=self._parse_metric_stats(analytics.get("temperature")),
                    )
                self.grouped_analytics.set_data(grouped_data)
            else:
                grouped_data = self._build_grouped_equipment_analytics_data(data)
                self.grouped_analytics.set_data(grouped_data)

            # Charts grid
            summary = self.build_charts_grid_summary(data)
            self.advanced.set_summary(summary)
        else:
            # Clear UI or show empty state
            self.advanced.set_summary(None)
            self.stat_summary.set_data(None)
            self.corr_insights.set_matrix({})
            self.conditional_analysis.set_data(None)
            self.distribution_analysis.set_data(None)
            self.equipment_ranking.set_data(None)
            self.grouped_analytics.set_data(None)

    def _parse_metric_stats(self, data: Optional[Dict[str, Any]]) -> MetricStats:
        if not data:
            return MetricStats(0, 0, 0, 0)
        return MetricStats(
            mean=data.get("mean", 0),
            std=data.get("std", 0),
            min=data.get("min", 0),
            max=data.get("max", 0),
        )

    def _parse_statistical_summary(self, data: Dict[str, Any]) -> StatisticalSummaryData:
        def parse_col(col: Dict[str, Any]) -> StatColumn:
            return StatColumn(
                count=col.get("count", 0),
                mean=col.get("mean", 0),
                std=col.get("std", 0),
                min=col.get("min", 0),
                q1=col.get("q1", 0),
                median=col.get("median", 0),
                q3=col.get("q3", 0),
                max=col.get("max", 0),
            )
        return StatisticalSummaryData(
            flowrate=parse_col(data.get("flowrate", {})),
            pressure=parse_col(data.get("pressure", {})),
            temperature=parse_col(data.get("temperature", {})),
        )

    def build_charts_grid_summary(self, records: List[Dict[str, Any]]) -> ChartsGridSummary:
        flow, pres, temp, types = [], [], [], []
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

    def build_statistical_summary(self, records: List[Dict[str, Any]]) -> StatisticalSummaryData:
        def stats(arr: List[float]) -> StatColumn:
            if not arr:
                return StatColumn(0, 0, 0, 0, 0, 0, 0, 0)
            arr_sorted = sorted(arr)
            n = len(arr)
            mean = sum(arr) / n
            std = (sum((x - mean) ** 2 for x in arr) / n) ** 0.5 if n > 1 else 0.0
            minv = arr_sorted[0]
            q1 = self._percentile(arr_sorted, 25)
            med = self._percentile(arr_sorted, 50)
            q3 = self._percentile(arr_sorted, 75)
            maxv = arr_sorted[-1]
            return StatColumn(
                count=n,
                mean=mean,
                std=std,
                min=minv,
                q1=q1,
                median=med,
                q3=q3,
                max=maxv,
            )

        flow, pres, temp = [], [], []
        for r in records:
            try:
                flow.append(float(r["Flowrate"]))
                pres.append(float(r["Pressure"]))
                temp.append(float(r["Temperature"]))
            except Exception:
                continue

        return StatisticalSummaryData(
            flowrate=stats(flow),
            pressure=stats(pres),
            temperature=stats(temp),
        )

    def _hist_counts(self, values: List[float], bins_count: int = 10, bin_edges: List[float] = None) -> Tuple[List[float], List[int]]:
        if not values:
            edges = [0.0, 1.0]
            return edges, [0]
        vmin, vmax = min(values), max(values)
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

    def _percentile(self, sorted_vals: List[float], p: float) -> float:
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

    def _boxplot_by_type(self, types: List[str], pressures: List[float]) -> Tuple[List[str], List[List[float]]]:
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

    def _pearson(self, a: List[float], b: List[float]) -> float:
        n = min(len(a), len(b))
        if n < 2:
            return 0.0
        a = a[:n]
        b = b[:n]
        ma = sum(a) / n
        mb = sum(b) / n
        num = da = db = 0.0
        for i in range(n):
            xa = a[i] - ma
            xb = b[i] - mb
            num += xa * xb
            da += xa * xa
            db += xb * xb
        if da == 0.0 or db == 0.0:
            return 0.0
        return num / ((da ** 0.5) * (db ** 0.5))

    def _correlation_matrix(self, flow: List[float], pres: List[float], temp: List[float]) -> List[CorrelationDatum]:
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

    def _build_correlation_matrix_dict(self, records: List[Dict[str, Any]]) -> dict:
        flow, pres, temp = [], [], []
        for r in records:
            try:
                flow.append(float(r["Flowrate"]))
                pres.append(float(r["Pressure"]))
                temp.append(float(r["Temperature"]))
            except Exception:
                continue
        labels = ["Flowrate", "Pressure", "Temperature"]
        series = {
            "Flowrate": flow,
            "Pressure": pres,
            "Temperature": temp,
        }
        matrix = {}
        for x in labels:
            matrix[x] = {}
            for y in labels:
                v = 1.0 if x == y else self._pearson(series[x], series[y])
                matrix[x][y] = float(v)
        return matrix

    def _build_conditional_analysis_data(self, records: List[Dict[str, Any]]) -> ConditionalAnalysisData:
        pressures = []
        for r in records:
            try:
                pressures.append(float(r["Pressure"]))
            except Exception:
                continue
        if not pressures:
            return None
        mean_pressure = sum(pressures) / len(pressures)
        filtered = [r for r in records if float(r.get("Pressure", 0)) > mean_pressure]
        if not filtered:
            return None
        flow_sum = pres_sum = temp_sum = 0.0
        for r in filtered:
            try:
                flow_sum += float(r["Flowrate"])
                pres_sum += float(r["Pressure"])
                temp_sum += float(r["Temperature"])
            except Exception:
                continue
        n = len(filtered)
        stats = ConditionalStats(
            flowrate=flow_sum / n if n else 0.0,
            pressure=pres_sum / n if n else 0.0,
            temperature=temp_sum / n if n else 0.0,
        )
        return ConditionalAnalysisData(
            conditionLabel="Pressure above dataset mean",
            totalRecords=n,
            stats=stats,
        )

    def _build_distribution_analysis_data(
        self,
        records: List[Dict[str, Any]],
        column: str = "Flowrate",
        title: str = "Flowrate",
        unit: str = " kg/h"
    ) -> Optional[DistributionAnalysisData]:
        values = []
        for r in records:
            try:
                values.append(float(r[column]))
            except Exception:
                continue
        if not values:
            return None
        arr = sorted(values)
        n = len(arr)
        minv = arr[0]
        q1 = self._percentile(arr, 25)
        med = self._percentile(arr, 50)
        q3 = self._percentile(arr, 75)
        maxv = arr[-1]
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = [v for v in arr if v < lower or v > upper]
        stats = DistributionStats(
            min=minv,
            q1=q1,
            median=med,
            q3=q3,
            max=maxv,
            outliers=outliers if outliers else None,
        )
        return DistributionAnalysisData(
            title=title,
            unit=unit,
            stats=stats,
        )

    def _build_equipment_ranking_data(self, records: List[Dict[str, Any]]) -> Optional[EquipmentRankingData]:
        ranking: EquipmentRankingData = {}
        for r in records:
            try:
                name = str(r["Equipment Name"])
                flow = float(r["Flowrate"])
                pres = float(r["Pressure"])
                temp = float(r["Temperature"])
                ranking[name] = PerformanceMetrics(
                    flowrate=flow,
                    pressure=pres,
                    temperature=temp,
                )
            except Exception:
                continue
        return ranking if ranking else None

    def _build_grouped_equipment_analytics_data(self, records: List[Dict[str, Any]]) -> Optional[GroupedAnalyticsData]:
        from collections import defaultdict

        groups = defaultdict(list)
        for r in records:
            try:
                typ = str(r["Type"])
                flow = float(r["Flowrate"])
                pres = float(r["Pressure"])
                temp = float(r["Temperature"])
                groups[typ].append((flow, pres, temp))
            except Exception:
                continue

        def stats(arr: List[float]) -> MetricStats:
            if not arr:
                return MetricStats(0, 0, 0, 0)
            n = len(arr)
            mean = sum(arr) / n
            std = (sum((x - mean) ** 2 for x in arr) / n) ** 0.5 if n > 1 else 0.0
            minv = min(arr)
            maxv = max(arr)
            return MetricStats(mean=mean, std=std, min=minv, max=maxv)

        result: GroupedAnalyticsData = {}
        for typ, vals in groups.items():
            flows = [v[0] for v in vals]
            press = [v[1] for v in vals]
            temps = [v[2] for v in vals]
            result[typ] = EquipmentAnalytics(
                flowrate=stats(flows),
                pressure=stats(press),
                temperature=stats(temps),
            )
        return result if result else None

    def logout(self):
        logout_user()
        self.app.show_login()