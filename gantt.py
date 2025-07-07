import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import timedelta
from pathlib import Path


def export_gantt_chart(df, filename="mowing_team_schedule.xlsx"):
    df = df.copy()

    if df.empty:
        print("No data to generate Gantt chart.")
        return

    # Ensure datetime and numeric fields are correct
    df["Start"] = pd.to_datetime(df["Date"], errors='coerce')
    df["Estimated Hours"] = pd.to_numeric(df["Estimated Hours"], errors='coerce')
    df = df.dropna(subset=["Start", "Estimated Hours"])

    if df.empty:
        print("No valid data after date/hour parsing.")
        return

    df["End"] = df["Start"] + pd.to_timedelta(df["Estimated Hours"], unit="h")
    df["Duration"] = (df["End"] - df["Start"]).dt.total_seconds() / 3600
    df["Label"] = df["Park"] + " (" + df["split_part"].astype(str) + ")"

    # Consistent color by team
    teams = sorted(df["Team"].unique())
    team_color_map = {team: plt.cm.tab20(i % 20) for i, team in enumerate(teams)}

    # Y positions
    df = df.sort_values(by=["Team", "Start", "Label"]).reset_index(drop=True)
    y_pos = list(range(len(df)))[::-1]  # top-to-bottom
    fig_height = max(2, 0.5 * len(df) + 2)
    fig, ax = plt.subplots(figsize=(15, fig_height))

    for i, (idx, row) in enumerate(df.iterrows()):
        edge_color = "red" if row["Overtime"] else "black"
        ax.barh(
            y=y_pos[i],
            left=row["Start"],
            width=row["End"] - row["Start"],
            height=0.4,
            color=team_color_map.get(row["Team"], "gray"),
            edgecolor=edge_color
        )
        ax.text(
            row["Start"] + timedelta(hours=row["Duration"] / 2),
            y_pos[i],
            row["Label"],
            va="center",
            ha="center",
            fontsize=8,
            color="black"
        )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(df["Label"])
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.xticks(rotation=45)
    ax.set_xlabel("Date")
    ax.set_title("Mowing Gantt Chart")
    plt.tight_layout()
    plt.grid(axis='x', linestyle='--', alpha=0.3)

    # Derive image name from Excel filename
    img_file = Path(filename).with_suffix('.gantt.png')
    plt.savefig(img_file, dpi=150)
    plt.close()

    print(f"✅ Gantt chart saved to: {img_file}")
