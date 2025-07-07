import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
from pathlib import Path


def export_gantt_chart(df, filename="mowing_team_schedule.xlsx"):
    df = df.copy()
    if df.empty:
        print("No data to generate calendar Gantt chart.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df["Estimated Hours"] = pd.to_numeric(df["Estimated Hours"], errors='coerce')
    df.dropna(subset=["Date", "Estimated Hours"], inplace=True)

    if df.empty:
        print("No valid data after parsing.")
        return

    df["Week"] = df["Date"].dt.isocalendar().week
    df["Weekday"] = df["Date"].dt.weekday  # Monday=0
    df["Label"] = df["Park"] + " (" + df["split_part"].astype(str) + ")"

    teams = sorted(df["Team"].unique())
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    team_color_map = {team: plt.cm.tab20(i % 20) for i, team in enumerate(teams)}

    spacing = 0.15  # vertical space per job label
    min_row_height = 1.0  # minimum row height (inches)
    padding = 0.5  # padding in inches per row

    width_per_day = 3  # width in inches per weekday column
    min_col_width = 2  # minimum width if you want to scale per workload (optional)

    # Calculate max jobs stacked per day for each team (for row height)
    team_row_heights = []
    for team in teams:
        team_df = df[df["Team"] == team]
        max_jobs = 0
        for day in range(len(weekdays)):
            n_jobs = len(team_df[team_df["Weekday"] == day])
            if n_jobs > max_jobs:
                max_jobs = n_jobs
        row_height = max(min_row_height, spacing * max_jobs + padding)
        team_row_heights.append(row_height)

    # For columns, here we keep equal widths, but you could calculate widths based on workload
    col_widths = [width_per_day] * len(weekdays)

    total_height = sum(team_row_heights)
    total_width = sum(col_widths)

    fig = plt.figure(figsize=(total_width, total_height), constrained_layout=True)
    gs = gridspec.GridSpec(
        nrows=len(teams),
        ncols=len(weekdays),
        height_ratios=team_row_heights,
        width_ratios=col_widths,
        figure=fig
    )

    for i, team in enumerate(teams):
        team_df = df[df["Team"] == team]
        for j, day in enumerate(range(len(weekdays))):
            ax = fig.add_subplot(gs[i, j])
            day_jobs = team_df[team_df["Weekday"] == day]
            items = day_jobs.sort_values("Date")

            n_jobs = len(items)
            y_start = min(0.95, spacing * n_jobs + 0.05)
            y = y_start

            for _, row in items.iterrows():
                edge_color = "red" if row.get("Overtime", False) else "black"
                ax.text(
                    0.5,
                    y,
                    f"{row['Label']}\n{row['Estimated Hours']}h",
                    ha='center',
                    va='top',
                    fontsize=8,
                    color="black",
                    bbox=dict(
                        boxstyle="round,pad=0.2",
                        facecolor=team_color_map[team],
                        edgecolor=edge_color
                    )
                )
                y -= spacing

            ax.set_xticks([])
            ax.set_yticks([])
            if i == 0:
                ax.set_title(weekdays[j])
            if j == 0:
                ax.set_ylabel(team, rotation=0, ha='right', va='center', fontsize=8)

    plt.suptitle("Calendar-style Gantt Chart (by Team and Day)", fontsize=14)

    out_file = Path(filename).with_suffix('.calendar_gantt.png')
    plt.savefig(out_file, dpi=150)
    plt.close()
    print(f"✅ Calendar-style Gantt chart saved to: {out_file}")
