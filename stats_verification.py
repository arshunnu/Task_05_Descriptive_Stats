"""
stats_verification.py
---------------------
Generates descriptive statistics for the SU Women’s Lacrosse 2025 dataset
and outputs results to an Excel report only.

Usage:
  python stats_verification.py
Output:
  - ground_truth_report.xlsx
"""

import argparse
from pathlib import Path
import pandas as pd

REQUIRED_COLS = ["Date", "Opponent", "Location", "Result", "Goals_For", "Goals_Against"]

# ✅ Your dataset path
DEFAULT_FILE = r"C:\Users\Arshunnu Bare\Desktop\SEM4\RA Tasks\Task 5\SU_Womens_Lacrosse_2025.xlsx"

def load_frame(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    if path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(path)
    elif path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        raise ValueError("Unsupported file type. Use .xlsx or .csv")

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Win"] = df["Result"].astype(str).str.startswith("W")
    df["Loss"] = df["Result"].astype(str).str.startswith("L")
    df["Goal_Diff"] = df["Goals_For"] - df["Goals_Against"]
    return df


def compute_ground_truth(df: pd.DataFrame) -> dict:
    home = df[df["Location"] == "Home"]
    away = df[df["Location"] == "Away"]

    gt = {
        "games_played": int(len(df)),
        "overall": {
            "wins": int(df["Win"].sum()),
            "losses": int(df["Loss"].sum())
        },
        "home": {
            "wins": int(home["Win"].sum()),
            "losses": int(home["Loss"].sum()),
            "games": int(len(home))
        },
        "away": {
            "wins": int(away["Win"].sum()),
            "losses": int(away["Loss"].sum()),
            "games": int(len(away))
        },
        "averages": {
            "goals_for": float(df["Goals_For"].mean()),
            "goals_against": float(df["Goals_Against"].mean()),
            "goal_diff": float((df["Goals_For"] - df["Goals_Against"]).mean())
        },
        "losses_sorted_by_margin": df[df["Loss"]].sort_values("Goal_Diff").assign(Margin=lambda x: -x["Goal_Diff"])[
            ["Date", "Opponent", "Location", "Result", "Goals_For", "Goals_Against", "Goal_Diff"]
        ],
        "wins_sorted_by_margin": df[df["Win"]].sort_values("Goal_Diff", ascending=False)[
            ["Date", "Opponent", "Location", "Result", "Goals_For", "Goals_Against", "Goal_Diff"]
        ],
        "biggest_win": df.loc[df["Goal_Diff"].idxmax()],
        "toughest_loss": df.loc[df["Goal_Diff"].idxmin()]
    }
    return gt


def export_to_excel(gt: dict, out_path: str):
    """Write summary, wins, losses, and highlights to Excel"""
    summary_df = pd.DataFrame([
        {"Metric": "Games Played", "Value": gt["games_played"]},
        {"Metric": "Overall Record", "Value": f'{gt["overall"]["wins"]}-{gt["overall"]["losses"]}'},
        {"Metric": "Home Record", "Value": f'{gt["home"]["wins"]}-{gt["home"]["losses"]}'},
        {"Metric": "Away Record", "Value": f'{gt["away"]["wins"]}-{gt["away"]["losses"]}'},
        {"Metric": "Avg Goals For", "Value": round(gt["averages"]["goals_for"], 2)},
        {"Metric": "Avg Goals Against", "Value": round(gt["averages"]["goals_against"], 2)},
        {"Metric": "Avg Goal Diff", "Value": round(gt["averages"]["goal_diff"], 2)},
    ])

    # Combine highlights
    highlights_df = pd.concat([
        pd.DataFrame([gt["biggest_win"]]).assign(Type="Biggest Win"),
        pd.DataFrame([gt["toughest_loss"]]).assign(Type="Toughest Loss")
    ], ignore_index=True)

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        gt["wins_sorted_by_margin"].to_excel(writer, sheet_name="Wins_Detail", index=False)
        gt["losses_sorted_by_margin"].to_excel(writer, sheet_name="Losses_Detail", index=False)
        highlights_df.to_excel(writer, sheet_name="Highlights", index=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=str, default=DEFAULT_FILE, help="Path to dataset (.xlsx or .csv)")
    ap.add_argument("--report_xlsx", type=str, default="ground_truth_report.xlsx", help="Excel output file")
    args = ap.parse_args()

    df = load_frame(Path(args.file))
    gt = compute_ground_truth(df)

    export_to_excel(gt, args.report_xlsx)

    print(f"✅ Excel report generated successfully: {args.report_xlsx}")
    print(f"Games: {gt['games_played']} | Wins: {gt['overall']['wins']} | Losses: {gt['overall']['losses']}")


if __name__ == "__main__":
    main()
