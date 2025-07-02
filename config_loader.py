
import json
from datetime import date

def load_config(config_path):
    with open(config_path) as f:
        config = json.load(f)
    config["START_DATE"] = date.fromisoformat(config["START_DATE"])
    config["PUBLIC_HOLIDAYS"] = {date.fromisoformat(d) for d in config["PUBLIC_HOLIDAYS"]}
    config["BAD_WEATHER_DAYS"] = {date.fromisoformat(d) for d in config.get("BAD_WEATHER_DAYS", [])}
    config["SKIPPED_DATES"] = config["PUBLIC_HOLIDAYS"] | config["BAD_WEATHER_DAYS"]
    config["DEPENDENCIES"] = config.get("DEPENDENCIES", {})
    config["HISTORICAL_HOURS"] = config.get("HISTORICAL_HOURS", {})
    return config
