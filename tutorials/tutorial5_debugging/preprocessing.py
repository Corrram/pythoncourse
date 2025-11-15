from typing import List, Dict, Optional
import math


def to_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def to_float(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def clean_participants(raw: List[Dict[str, Optional[str]]]) -> List[Dict]:
    """
    Clean and normalize participant records.

    Output record:
        - participant_id: int
        - name: str
        - group: str ('control' or 'treatment')
        - age: int or None
    """
    cleaned: List[Dict] = []

    for row in raw:
        pid = to_int(row.get("participant_id"))
        name = row.get("name")
        group = row.get("group")
        age = to_int(row.get("age"))

        if pid is None or not name or not group:
            continue

        group_norm = group.strip().lower()
        if group_norm not in {"control", "treatment"}:
            continue

        cleaned.append(
            {
                "participant_id": pid,
                "name": name.strip(),
                "group": group_norm,
                "age": age,
            }
        )

    return cleaned


def clean_measurements(raw: List[Dict[str, Optional[str]]]) -> List[Dict]:
    """
    Clean measurement records.

    Output record:
        - participant_id: int
        - session: int
        - score: float
    """
    cleaned: List[Dict] = []

    for row in raw:
        pid = to_int(row.get("participant_id"))
        session = to_int(row.get("session"))
        score = to_float(row.get("score"))

        if pid is None or session is None or score is None or math.isnan(score):
            continue

        cleaned.append(
            {
                "participant_id": pid,
                "session": session,
                "score": score,
            }
        )

    return cleaned
