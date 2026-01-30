import pandas as pd
import numpy as np

def analyze_equipment_json(records: list):
    df = pd.DataFrame(records)

    df = df.rename(columns={
        "Equipment Name": "name",
        "Type": "type",
        "Flowrate": "flowrate",
        "Pressure": "pressure",
        "Temperature": "temperature",
    })

    for col in ["flowrate", "pressure", "temperature"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    total_count = len(df)

    avg_flowrate = df["flowrate"].mean()
    avg_pressure = df["pressure"].mean()
    avg_temperature = df["temperature"].mean()

    type_distribution = df["type"].value_counts().to_dict()

    scatter_points = df.sample(min(200, len(df))).apply(
        lambda r: {
            "x": round(r["flowrate"], 2),
            "y": round(r["pressure"], 2),
            "t": round(r["temperature"], 2),
        },
        axis=1
    ).tolist()

    flow_bins = pd.cut(df["flowrate"], bins=5)
    temp_bins = pd.cut(df["temperature"], bins=5)

    histogram = {
        "labels": [str(i) for i in flow_bins.cat.categories],
        "flowrate": flow_bins.value_counts().sort_index().tolist(),
        "temperature": temp_bins.value_counts().sort_index().tolist(),
    }

    boxplot = {
        "labels": ["Flowrate", "Pressure", "Temperature"],
        "values": [
            df["flowrate"].quantile([0, .25, .5, .75, 1]).tolist(),
            df["pressure"].quantile([0, .25, .5, .75, 1]).tolist(),
            df["temperature"].quantile([0, .25, .5, .75, 1]).tolist(),
        ]
    }

    corr = df[["flowrate", "pressure", "temperature"]].corr()
    correlation = [
        {"x": i, "y": j, "v": round(corr.loc[i, j], 4)}
        for i in corr.columns
        for j in corr.columns
    ]

    def stats(col):
        return {
            "count": int(df[col].count()),
            "mean": df[col].mean(),
            "std": df[col].std(),
            "min": df[col].min(),
            "q1": df[col].quantile(0.25),
            "median": df[col].median(),
            "q3": df[col].quantile(0.75),
            "max": df[col].max(),
        }

    statistical_summary = {
        "data": {
            "flowrate": stats("flowrate"),
            "pressure": stats("pressure"),
            "temperature": stats("temperature"),
        }
    }

    grouped = {}
    for t, g in df.groupby("type"):
        grouped[t] = {
            "flowrate": stats("flowrate"),
            "pressure": stats("pressure"),
            "temperature": stats("temperature"),
        }

    return {
        "total_count": total_count,
        "avg_flowrate": avg_flowrate,
        "avg_pressure": avg_pressure,
        "avg_temperature": avg_temperature,
        "type_distribution": type_distribution,
        "scatter_points": scatter_points,
        "histogram": histogram,
        "boxplot": boxplot,
        "correlation": correlation,
        "StatisticalSummary": statistical_summary,
        "GroupedEquipmentAnalytics": grouped,
        "data": df.head(20).to_dict(orient="records"),
    }