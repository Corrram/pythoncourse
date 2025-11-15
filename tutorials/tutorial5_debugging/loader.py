import csv
from typing import List, Dict, Optional


def load_participants(csv_path: str) -> List[Dict[str, Optional[str]]]:
    """
    Load participant information from CSV.

    Columns:
        - participant_id
        - name
        - group
        - age
    """
    records: List[Dict[str, Optional[str]]] = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(
                {
                    "participant_id": row.get("participant_id") or None,
                    "name": row.get("name") or None,
                    "group": row.get("group") or None,
                    "age": row.get("age") or None,
                }
            )

    return records


def load_measurements(csv_path: str) -> List[Dict[str, Optional[str]]]:
    """
    Load measurement data from CSV.

    Columns:
        - participant_id
        - session
        - score
    """
    records: List[Dict[str, Optional[str]]] = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(
                {
                    "participant_id": row.get("participant_id") or None,
                    "session": row.get("session") or None,
                    "score": row.get("score") or None,
                }
            )

    return records
