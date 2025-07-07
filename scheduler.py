import heapq
import pandas as pd
from utils import get_nth_working_day


class MowingScheduler:
    def __init__(self, config, parks):
        self.config = config
        self.parks = parks
        self.jobs = {}
        self.completed_jobs = set()

    def build_team_heap(self, team_status, team_list):
        heap = []
        for team in team_list:
            status = team_status[team]
            heap.append((status["total_hours_assigned"], len(status["parks_assigned_set"]), team))
        heapq.heapify(heap)
        return heap

    def assign_parks(self):
        parks_sorted = sorted(self.parks, key=lambda x: (-x.get("priority", 0), x["area_sqm"]))
        all_teams = sorted({t for group in self.config["TEAM_NAME_MAPPING"].values() for t in group})
        self.jobs = {t: [] for t in all_teams}
        team_status = {
            t: {
                "team_name": t,
                "current_day": 1,
                "hours_assigned_today": 0,
                "total_hours_assigned": self.config["HISTORICAL_HOURS"].get(t, 0),
                "weekly_hours": {},
                "parks_assigned_set": set(),
            } for t in all_teams
        }

        job_counter = 0

        for park in parks_sorted:
            if park["area_sqm"] <= 0:
                continue
            if any(dep not in self.completed_jobs for dep in self.config["DEPENDENCIES"].get(park["name"], [])):
                continue

            total_time = (park["area_sqm"] / self.config["DEFAULT_MOWING_RATE_SQM_PER_HOUR"]) * (1 + self.config["DEFAULT_BUFFER"])
            time_remaining = total_time
            split_part = 1
            job_counter += 1
            job_id = f"{park['name'].replace(' ', '_')}_{job_counter}"
            allowed_combined = self.config["SUBURB_TO_COMBINED_TEAM"].get(park["suburb"], self.config["TEAM_NAME_MAPPING"].keys())
            allowed_individual = [t for group in allowed_combined for t in self.config["TEAM_NAME_MAPPING"][group]]

            while time_remaining > 0:
                if not allowed_individual:
                    break
                min_day = min(team_status[t]["current_day"] for t in allowed_individual)
                work_date = get_nth_working_day(self.config["START_DATE"], min_day, self.config["SKIPPED_DATES"])
                week = (min_day - 1) // self.config["DEFAULT_WORKDAYS_PER_WEEK"] + 1
                team_heap = self.build_team_heap(team_status, allowed_individual)
                assigned_any = False

                for _, _, t in sorted(team_heap):
                    status = team_status[t]
                    if status["current_day"] < min_day:
                        status["current_day"] = min_day
                        status["hours_assigned_today"] = 0
                    current_work_date = get_nth_working_day(self.config["START_DATE"], status["current_day"], self.config["SKIPPED_DATES"])
                    if current_work_date != work_date:
                        continue
                    max_week_hours = self.config["WEEKLY_HOUR_LIMITS"].get(t, float('inf'))
                    current_week_hours = status["weekly_hours"].get(week, 0)
                    available_today = self.config["DEFAULT_WORKDAY_HOURS"] - status["hours_assigned_today"]

                    overtime_flag = False
                    if available_today <= 0 and self.config["ALLOW_OVERTIME"]:
                        available_today = self.config["MAX_OVERTIME_HOURS_PER_DAY"]
                        overtime_flag = True
                    elif available_today <= 0:
                        continue

                    # Cap total daily hours including overtime
                    max_daily_hours = self.config["DEFAULT_WORKDAY_HOURS"]
                    if self.config["ALLOW_OVERTIME"]:
                        max_daily_hours += self.config["MAX_OVERTIME_HOURS_PER_DAY"]

                    remaining_daily_capacity = max_daily_hours - status["hours_assigned_today"]
                    if remaining_daily_capacity <= 0:
                        continue

                    available_total = min(available_today, max_week_hours - current_week_hours, remaining_daily_capacity)
                    if available_total <= 0:
                        continue

                    time_to_assign = min(available_total, time_remaining)

                    area_chunk = time_to_assign * self.config["DEFAULT_MOWING_RATE_SQM_PER_HOUR"] / (1 + self.config["DEFAULT_BUFFER"])

                    self.jobs[t].append({
                        "job_id": job_id,
                        "split_part": split_part,
                        "name": park["name"],
                        "suburb": park["suburb"],
                        "area_sqm": round(area_chunk, 2),
                        "estimated_hours": round(time_to_assign, 2),
                        "day": status["current_day"],
                        "date": work_date.isoformat(),
                        "overtime": overtime_flag and self.config["ALLOW_OVERTIME"],
                        "priority": park.get("priority", 0)
                    })

                    split_part += 1
                    status["hours_assigned_today"] += time_to_assign
                    status["total_hours_assigned"] += time_to_assign
                    status["weekly_hours"][week] = current_week_hours + time_to_assign
                    status["parks_assigned_set"].add(park["name"])
                    time_remaining -= time_to_assign
                    assigned_any = True

                    if time_remaining <= 0:
                        self.completed_jobs.add(park["name"])
                        break

                if not assigned_any:
                    for t in allowed_individual:
                        team_status[t]["current_day"] += 1
                        team_status[t]["hours_assigned_today"] = 0

        return self.jobs

    def export_jobs_to_df(self):
        rows = []
        for team, assignments in self.jobs.items():
            for job in assignments:
                rows.append({
                    "Team": team,
                    "Day": job["day"],
                    "Date": job["date"],
                    "Park": job["name"],
                    "Suburb": job["suburb"],
                    "Area (sqm)": job["area_sqm"],
                    "Estimated Hours": job["estimated_hours"],
                    "Overtime": job["overtime"],
                    "Priority": job.get("priority", 0),
                    "job_id": job["job_id"],
                    "split_part": job["split_part"]
                })
        df = pd.DataFrame(rows)
        df.sort_values(by=["Team", "Day"], inplace=True)
        return df

    def add_week_and_weekday(self, df):
        df = df.copy()
        df['Week'] = ((df['Day'] - 1) // self.config["DEFAULT_WORKDAYS_PER_WEEK"]) + 1
        df['Weekday'] = pd.to_datetime(df['Date']).dt.strftime('%a')
        return df

    def build_calendar(self, df, week_range=None):
        calendar = {}
        for _, row in df.iterrows():
            week = row['Week']
            if week_range and week not in week_range:
                continue
            team = row['Team']
            day = row['Weekday']
            text = f"{row['Park']} ({row['Estimated Hours']}h)"
            calendar.setdefault(team, {}).setdefault(week, {}).setdefault(day, []).append(text)

        all_weeks = sorted({w for t in calendar.values() for w in t})
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        rows = []

        for team in sorted(calendar):
            row = {"Team": team}
            for week in all_weeks:
                for day in weekdays:
                    key = f"W{week} {day}"
                    items = calendar.get(team, {}).get(week, {}).get(day, [])
                    row[key] = "\n".join(sorted(items))
            rows.append(row)
        return pd.DataFrame(rows)

    def generate_metrics(self, df):
        overtime = df["Overtime"].astype(bool)
        summary = df.groupby('Team').agg(
            Total_Parks=('Park', 'nunique'),
            Total_Area_Sqm=('Area (sqm)', 'sum'),
            Total_Hours=('Estimated Hours', 'sum'),
            Days_Worked=('Day', 'nunique'),
            Total_Overtime_Hours=('Estimated Hours', lambda x: x[overtime.loc[x.index]].sum())
        ).reset_index()
        summary["Avg_Hours_Per_Day"] = (summary["Total_Hours"] / summary["Days_Worked"]).round(2)
        return summary.round(2)
