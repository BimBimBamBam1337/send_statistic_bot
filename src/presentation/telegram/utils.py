from .constans import MONTHS


def transform_date(month: int):
    return f"{MONTHS[int(month) - 1]}"
