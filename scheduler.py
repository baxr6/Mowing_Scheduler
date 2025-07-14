
import argparse
import logging
import os
import sys
from pathlib import Path

# Automatically set working directory to script location
script_dir = Path(__file__).resolve().parent
os.chdir(script_dir)
sys.path.insert(0, str(script_dir))

from config_loader import load_config
from park_loader import load_parks_from_csv
from scheduler import MowingScheduler
from excel_export import export_to_excel
from gantt import export_gantt_chart

def parse_args():
    parser = argparse.ArgumentParser(description="Mowing Scheduler CLI")
    parser.add_argument("--csv", default="sample_parks_300.csv", help="CSV input file")
    parser.add_argument("--config", default="config.json", help="Config file")
    parser.add_argument("--weeks", nargs="*", type=int, help="Weeks to include in output")
    parser.add_argument("--output", default="mowing_team_schedule.xlsx", help="Output Excel filename")
    parser.add_argument("--test", action="store_true", help="Run unit tests")
    return parser.parse_args()

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")
    args = parse_args()

    if args.test:
        import unittest
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
        return

    config = load_config(args.config)
    parks = load_parks_from_csv(args.csv)

    scheduler = MowingScheduler(config, parks)
    scheduler.assign_parks()
    df_jobs = scheduler.export_jobs_to_df()
    df_jobs = scheduler.add_week_and_weekday(df_jobs)

    df_jobs_filtered = df_jobs[df_jobs["Week"].isin(args.weeks)] if args.weeks else df_jobs
    calendar_df = scheduler.build_calendar(df_jobs_filtered, args.weeks)
    metrics_df = scheduler.generate_metrics(df_jobs_filtered)

    export_to_excel(df_jobs_filtered, calendar_df, metrics_df, filename=args.output)
    export_gantt_chart(df_jobs_filtered, filename=args.output)

    logging.info("📅 Calendar View Preview:\n" + calendar_df.head().to_string(index=False))
    logging.info("📊 Metrics Summary:\n" + metrics_df.to_string(index=False))

if __name__ == "__main__":
    main()
