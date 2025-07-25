import isodate


def convert_duration_to_minutes_iso(duration_str: str) -> int:

    if not duration_str or duration_str == "N/A":
        return 0

    try:
        duration = isodate.parse_duration(duration_str)
        return int(duration.total_seconds() / 60)
    except:
        return 0
