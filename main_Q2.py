#!/usr/bin/env python3 
# Triple-quoted string to describe the purpose of the script
"""
HIT137 – Assignment 2 (Q2): Australian Temperature Analysis

Reads ALL .csv files in the `temperatures/` folder, computes:
1) Seasonal averages across all stations & all years
2) Station(s) with the largest temperature range
3) Station(s) with the smallest & largest temperature standard deviation

Writes results to:
- average_temp.txt
- largest_temp_range_station.txt
- temperature_stability_stations.txt
"""
# these lines import necessary modules - path/system level/data manipulation/hints
from pathlib import Path
import sys
import pandas as pd
from typing import Optional, Tuple, List, Dict

# paths for input and output files relative to script location
INPUT_FOLDER = Path(__file__).parent / "temperatures"
OUT_AVG = Path(__file__).parent / "average_temp.txt"
OUT_RANGE = Path(__file__).parent / "largest_temp_range_station.txt"
OUT_STABILITY = Path(__file__).parent / "temperature_stability_stations.txt"

# --------- Helpers --------- 
# This tries to find a column in the data frame that matches one of the names
# if contains = True, it looks for substings of exact match

def _find_column(df: pd.DataFrame, candidates: List[str], contains: bool=False) -> Optional[str]:
    cols = [c for c in df.columns]
    lower_map = {c.lower(): c for c in cols}
    if contains:
        # Return the first column whose lower-name contains any candidate substrings
        for c in cols:
            lc = c.lower()
            for cand in candidates:
                if cand in lc:
                    return c
        return None
    else:
        for cand in candidates:
            if cand in lower_map:
                return lower_map[cand]
        return None

def _season_from_month(month: int) -> str:
    # converts month number to an Australian Season
    # Australian seasons
    if month in (12, 1, 2):
        return "Summer"
    if month in (3, 4, 5):
        return "Autumn"
    if month in (6, 7, 8):
        return "Winter"
    return "Spring"  # 9,10,11

def _read_and_normalise_csv(path: Path) -> Optional[pd.DataFrame]:
    # Reads CSV files and normalizes to have three columns and handles missing columns
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"[WARN] Failed to read {path.name}: {e}")
        return None

    if df.empty:
        print(f"[WARN] Skipping empty file: {path.name}")
        return None

    # Auto-detect columns
    station_col = _find_column(df, ["station", "station_id", "stationname", "station_name", "site", "site_name"])
    date_col = _find_column(df, ["date", "timestamp", "datetime", "time"])
    temp_col = _find_column(df, ["temp"], contains=True)

    missing = []
    if station_col is None:
        missing.append("Station")
    if date_col is None:
        missing.append("Date/Time")
    if temp_col is None:
        missing.append("Temperature")

    if missing:
        print(f"[WARN] Skipping {path.name}: Missing required column(s): {', '.join(missing)}")
        return None

    # Parse date
    try:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    except Exception as e:
        print(f"[WARN] Could not parse dates in {path.name}: {e}")
        return None

    # Build normalized DataFrame
    out = pd.DataFrame({
        "station": df[station_col].astype(str),
        "date": df[date_col],
        "temp": pd.to_numeric(df[temp_col], errors="coerce")
    })

    # Drop rows without valid date or temp
    out = out.dropna(subset=["date", "temp"])

    if out.empty:
        print(f"[WARN] No valid rows after cleaning in {path.name}")
        return None

    return out

def load_all_data(input_folder: Path) -> pd.DataFrame:
    # Loads all CSV files in the temperatures/folder
    all_rows = []
    csv_files = sorted(input_folder.glob("*.csv"))
    if not csv_files:
        print(f"[ERROR] No CSV files found in {input_folder}. Put your yearly CSVs there.")
        return pd.DataFrame(columns=["station", "date", "temp"])

    for f in csv_files:
        norm = _read_and_normalise_csv(f)
        if norm is not None and not norm.empty:
            all_rows.append(norm)

    if not all_rows:
        print("[ERROR] No valid data could be loaded from the CSVs.")
        return pd.DataFrame(columns=["station", "date", "temp"])

    df = pd.concat(all_rows, ignore_index=True)
    return df

# --------- Analyses ---------

def compute_seasonal_averages(df: pd.DataFrame) -> pd.Series:
    # Adds season column based on the month and computes the average temperature per season
    df = df.copy()
    df["season"] = df["date"].dt.month.apply(_season_from_month)
    # drop NaN temps already handled; group and mean
    seasonal = df.groupby("season")["temp"].mean()
    # Ensure order Summer, Autumn, Winter, Spring
    order = ["Summer", "Autumn", "Winter", "Spring"]
    seasonal = seasonal.reindex(order)
    return seasonal

def compute_temperature_ranges(df: pd.DataFrame) -> pd.DataFrame:
    # Calculates the temperature range (max - Min) for each station
    g = df.groupby("station")["temp"]
    stats = g.agg(temp_min="min", temp_max="max")
    stats["range"] = stats["temp_max"] - stats["temp_min"]
    return stats.sort_values("range", ascending=False) # type: ignore

def compute_temperature_stability(df: pd.DataFrame) -> pd.Series:
    # computes the standard deviation of temperatures for each station
    stds = df.groupby("station")["temp"].std(ddof=1)  # sample std dev
    return stds

# --------- Writers ---------

def write_average_temp(seasonal: pd.Series, out_path: Path) -> None:
    # writes the season average temperature to a text file
    lines = []
    for season in ["Summer", "Autumn", "Winter", "Spring"]:
        val = seasonal.get(season, float("nan"))
        if pd.isna(val):
            lines.append(f"{season}: N/A")
        else:
            lines.append(f"{season}: {val:.1f}°C")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote seasonal averages to {out_path.name}")

def write_largest_range(station_stats: pd.DataFrame, out_path: Path) -> None:
    # Finds the stations with the largest temperatures and writes to a file
    if station_stats.empty:
        out_path.write_text("No data available.", encoding="utf-8")
        print(f"[OK] Wrote largest temperature range to {out_path.name} (empty)")
        return
    max_range = station_stats["range"].max()
    winners = station_stats[station_stats["range"] == max_range]
    lines = []
    for station, row in winners.iterrows():
        lines.append(f"{station}: Range {row['range']:.1f}°C (Max: {row['temp_max']:.1f}°C, Min: {row['temp_min']:.1f}°C)")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote largest temp range stations to {out_path.name}")

def write_stability(stds: pd.Series, out_path: Path) -> None:
    # identifies the most stable and most variable stations based on the standar deviation and writes to file
    if stds.empty:
        out_path.write_text("No data available.", encoding="utf-8")
        print(f"[OK] Wrote stability to {out_path.name} (empty)")
        return

    min_std = stds.min()
    max_std = stds.max()
    most_stable = stds[stds == min_std].sort_index()
    most_variable = stds[stds == max_std].sort_index()

    lines = ["Most Stable:"]
    for station, val in most_stable.items():
        lines.append(f"- {station}: StdDev {val:.1f}°C")
    lines.append("")
    lines.append("Most Variable:")
    for station, val in most_variable.items():
        lines.append(f"- {station}: StdDev {val:.1f}°C")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Wrote temperature stability stations to {out_path.name}")

def main():
    # Arranges the whole process - Loads data/Computes seasonal Averages/Computes temperature ranges and write them/computes stability and writes it
    df = load_all_data(INPUT_FOLDER)
    if df.empty:
        print("[FATAL] No valid data to process. Exiting.")
        sys.exit(1)

    # Seasonal Averages
    seasonal = compute_seasonal_averages(df)
    write_average_temp(seasonal, OUT_AVG)

    # Largest Temperature Range
    station_stats = compute_temperature_ranges(df)
    write_largest_range(station_stats, OUT_RANGE)

    # Temperature Stability
    stds = compute_temperature_stability(df)
    write_stability(stds, OUT_STABILITY)

if __name__ == "__main__":
    main()

