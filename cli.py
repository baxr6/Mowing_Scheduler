import argparse
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

# Automatically set working directory to script location
script_dir = Path(__file__).resolve().parent
os.chdir(script_dir)
sys.path.insert(0, str(script_dir))

from config_loader import load_config
from park_loader import load_parks_from_csv
from scheduler import MowingScheduler
from excel_export import export_to_excel
from gantt import export_gantt_chart


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mowing Scheduler CLI")
    parser.add_argument("--csv", default="sample_parks_300.csv", help="CSV input file")
    parser.add_argument("--config", default="config.json", help="Config file")
    parser.add_argument(
        "--weeks",
        nargs="*",
        type=int,
        help="Weeks to include in output (e.g. --weeks 1 2 3). If omitted, all weeks are included.",
    )
    parser.add_argument("--output", default="mowing_team_schedule.xlsx", help="Output Excel filename")
    parser.add_argument("--test", action="store_true", help="Run unit tests")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging (DEBUG level)"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s: %(message)s")

    if args.test:
        import unittest
        unittest.main(argv=["first-arg-is-ignored"], exit=False)
        return

    try:
        config = load_config(args.config)
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        return

    try:
        parks = load_parks_from_csv(args.csv)
    except Exception as e:
        logging.error(f"Failed to load parks from CSV: {e}")
        return

    scheduler = MowingScheduler(config, parks)
    scheduler.assign_parks()
    df_jobs = scheduler.export_jobs_to_df()
    df_jobs = scheduler.add_week_and_weekday(df_jobs)

    # Filter weeks if specified
    if args.weeks:
        missing_weeks = set(args.weeks) - set(df_jobs["Week"].unique())
        if missing_weeks:
            logging.warning(f"Requested weeks {sorted(missing_weeks)} not found in data.")
        df_jobs_filtered = df_jobs[df_jobs["Week"].isin(args.weeks)]
    else:
        df_jobs_filtered = df_jobs

    calendar_df = scheduler.build_calendar(df_jobs_filtered, args.weeks)
    metrics_df = scheduler.generate_metrics(df_jobs_filtered)

    export_to_excel(df_jobs_filtered, calendar_df, metrics_df, filename=args.output)
    export_gantt_chart(df_jobs_filtered, filename=args.output)

    logging.info("📅 Calendar View Preview:\n" + calendar_df.head().to_string(index=False))
    logging.info("📊 Metrics Summary:\n" + metrics_df.to_string(index=False))


if __name__ == "__main__":
    main()