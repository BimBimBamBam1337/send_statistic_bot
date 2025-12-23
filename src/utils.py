import re


def to_int(value: str) -> int | None:
    if not value or value == "#DIV/0!":
        return None
    digits = re.sub(r"[^\d]", "", value)
    return int(digits) if digits else 0


def to_date_dict(data: list[list[str]]) -> dict[str, dict[str, int | None]]:
    result: dict[str, dict[str, int | None]] = {}

    for row in data:
        for i in range(0, len(row), 4):
            date_ = "0" + row[i].strip() if len(row[i].strip()) == 4 else row[i].strip()

            if not date_ or not date_[0].isdigit():
                continue

            plan = row[i + 1].strip() if i + 1 < len(row) else ""
            fact = row[i + 2].strip() if i + 2 < len(row) else ""
            percent = row[i + 3].strip() if i + 3 < len(row) else ""

            result[date_] = {
                "plan": to_int(plan),
                "fact": to_int(fact),
                "percent": to_int(percent),
            }

    return result
