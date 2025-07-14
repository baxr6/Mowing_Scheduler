import json
from datetime import date, timedelta

def load_config(config_path):
    with open(config_path) as f:
        config = json.load(f)
    config["START_DATE"] = date.fromisoformat(config["START_DATE"])
    config["PUBLIC_HOLIDAYS"] = {date.fromisoformat(d) for d in config["PUBLIC_HOLIDAYS"]}
    config["BAD_WEATHER_DAYS"] = {date.fromisoformat(d) for d in config.get("BAD_WEATHER_DAYS", [])}

    # Automatically add Sundays as skipped dates
    # Find a range to cover e.g. next 365 days from START_DATE
    skipped = config["PUBLIC_HOLIDAYS"] | config["BAD_WEATHER_DAYS"]
    start = config["START_DATE"]
    end = start + timedelta(days=365)
    current = start
    while current <= end:
        if current.weekday() == 6:  # Sunday == 6
            skipped.add(current)
        current += timedelta(days=1)

    config["SKIPPED_DATES"] = skipped
    config["DEPENDENCIES"] = config.get("DEPENDENCIES", {})
    config["HISTORICAL_HOURS"] = config.get("HISTORICAL_HOURS", {})
    return config
