# 🏞️ Mowing Scheduler

A Python-based scheduling tool to optimize the assignment of mowing tasks across teams, generate Excel schedules, and visualize work allocation with Gantt charts.

---

## 🚀 Features

- 📊 **Intelligent Scheduling** based on area, priority, and team availability
- 📅 **Calendar and Gantt Chart** generation
- 📁 **CSV Input + Configurable JSON settings**
- 📤 **Exports Excel spreadsheet** with:
  - Job assignments
  - Calendar view
  - Team performance metrics
- ⚙️ **Supports job dependencies and team mappings**
- 🧪 Optional unit test runner

---

## 📂 Project Structure

scheduling_class/

├── cli.py # Command-line entry point

├── scheduler.py # Core logic for job scheduling

├── gantt.py # Gantt chart visualization

├── excel_export.py # Excel export functionality

├── config_loader.py # Loads JSON configuration

├── park_loader.py # Loads parks from CSV

├── utils.py # Helper functions (e.g., working days)

├── config.json # Sample configuration

├── sample_parks_300.csv # Sample input park data


---

## 🛠️ Requirements

- Python 3.8+
- pandas
- openpyxl
- matplotlib

Install dependencies:

```bash
pip install -r requirements.txt

📈 How to Use

python scheduling_class/cli.py --csv sample_parks_300.csv --config config.json --output schedule.xlsx

Optional Arguments:

    --weeks 1 2 3 : Filter output to specific weeks

    --test : Run unit tests

📋 Configuration (config.json)

Example fields:

{
  "DEFAULT_MOWING_RATE_SQM_PER_HOUR": 1200,
  "DEFAULT_WORKDAY_HOURS": 6,
  "DEFAULT_WORKDAYS_PER_WEEK": 6,
  "DEFAULT_BUFFER": 0.05,
  "ALLOW_OVERTIME": false,
  "MAX_OVERTIME_HOURS_PER_DAY": 2,
  "START_DATE": "2025-07-07",
  "PUBLIC_HOLIDAYS": ["2025-07-08", "2025-07-26"],
  "BAD_WEATHER_DAYS": ["2025-07-08", "2025-07-26"],
  "TEAM_NAME_MAPPING": {
    "North": ["Team A", "Team B", "Team C", "Team D"],
    "South": ["Team E", "Team F", "Team G", "Team H"],
    "Central": ["Team I", "Team J", "Team K", "Team L"]
  },
  "SUBURB_TO_COMBINED_TEAM": {
    "Dinmore": ["North"],
    "Springfield": ["South"],
    "Riverview": ["Central"],
    "FlindersView": ["North", "Central"],
    "Raceview": ["South", "Central"]
  },
  "WEEK_RANGE_TO_INCLUDE": [1],
  "WEEKLY_HOUR_LIMITS": {
  "Team A": 38,
  "Team B": 38,
  "Team C": 38,
  "Team D": 38,
  "Team E": 38,
  "Team F": 38,
  "Team G": 38,
  "Team H": 38,
  "Team I": 38,
  "Team J": 38,
  "Team K": 38,
  "Team L": 38
}

}


📄 Input Data (sample_parks_300.csv)

CSV should include at least:

name,suburb,area_sqm
Central Park,Northside,2500
Riverside,Sunnyside,3000

📤 Output

The script generates:

    schedule.xlsx – Contains job list, calendar view, metrics

    schedule.xlsx_gantt.png – Gantt chart visualizing team schedules

🧪 Testing

To run the unit tests (if defined):

python scheduling_class/cli.py --test

📌 Notes

    Jobs with unmet dependencies will be skipped until resolved.

    Parks with area ≤ 0 are ignored.

    Teams are assigned using a heap-based load balancer for fairness.

📬 Contact

Maintained by deano.welch@gmail.com. Contributions welcome!
📄 License
