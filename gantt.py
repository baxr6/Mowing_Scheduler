import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import timedelta

def export_gantt_chart(df, filename="mowing_team_schedule.xlsx"):
    df = df.copy()
    df["Start"] = pd.to_datetime(df["Date"])
    df["End"] = df["Start"] + pd.to_timedelta(df["Estimated Hours"], unit="h")
    df["Duration"] = (df["End"] - df["Start"]).dt.total_seconds() / 3600
    df["Label"] = df["Park"] + " (" + df["split_part"].astype(str) + ")"

    fig, ax = plt.subplots(figsize=(15, 0.5 * len(df) + 2))
    y_pos = list(range(len(df)))[::-1]
    colors = plt.cm.tab20.colors

    for i, (idx, row) in enumerate(df.iterrows()):
        ax.barh(
            y=y_pos[i],
            left=row["Start"],
            width=row["End"] - row["Start"],
            height=0.4,
            color=colors[i % len(colors)],
            edgecolor="black"
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

    # Save chart image (optional): add to Excel or standalone
    img_file = "gantt_chart.png"
    plt.savefig(img_file)
    plt.close()
