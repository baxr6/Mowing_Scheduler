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
  "TEAM_NAME_MAPPING": {
    "North": ["TeamA", "TeamB"],
    "South": ["TeamC"]
  },
  "HISTORICAL_HOURS": {
    "TeamA": 20,
    "TeamB": 15
  },
  "DEFAULT_MOWING_RATE_SQM_PER_HOUR": 1000,
  "DEFAULT_BUFFER": 0.15,
  "DEPENDENCIES": {
    "Park 2": ["Park 1"]
  }
}

📄 Input Data (sample_parks_300.csv)

CSV should include at least:

name,suburb,area_sqm,priority
Central Park,Northside,2500,2
Riverside,Sunnyside,3000,1

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
