MONTHS = [
    "Verdanir","Emberfall","Duskwatch","Glimmerwane","Brightreach",
    "Stormrest","Hollowshade","Deepmoor","Frostmere","Starwake"
]

def parse_date(date_text: str):
    """
    Accepts formats like "12 Glimmerwane 104" or "12 Glimmerwane, 104".
    Returns (day, month, year, world_day) with month as 1-10.
    """
    if not date_text:
        return None, None, None, None
    s = date_text.replace(",", " ").split()
    # naive parse
    day = int(s[0])
    month_name = s[1]
    year = int(s[2])
    month_index = MONTHS.index(month_name) + 1
    world_day = (year * 360) + ((month_index - 1) * 36) + day
    return day, month_index, year, world_day
