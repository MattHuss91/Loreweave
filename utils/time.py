from typing import Tuple, Optional
from .db import query

def get_calendar():
    rows = query("SELECT month_id,name,days FROM calendar_months ORDER BY month_id")
    if rows:
        months = [(r["name"], r["days"]) for r in rows]
        return months
    return [
        ("Verdanir",36),("Emberfall",36),("Duskwatch",36),("Glimmerwane",36),("Brightreach",36),
        ("Stormrest",36),("Hollowshade",36),("Deepmoor",36),("Frostmere",36),("Starwake",36)
    ]

def parse_date(date_text: str) -> Tuple[Optional[int], Optional[int], Optional[int], Optional[int]]:
    if not date_text:
        return None, None, None, None
    try:
        s = date_text.replace(",", " ").split()
        day = int(s[0])
        month_name = s[1]
        year = int(s[2])
        months = get_calendar()
        names = [m[0] for m in months]
        if month_name not in names:
            return None, None, None, None
        month_index = names.index(month_name) + 1
        days_before = sum(months[i][1] for i in range(month_index-1))
        world_day = year * sum(m[1] for m in months) + days_before + day
        return day, month_index, year, world_day
    except Exception:
        return None, None, None, None
