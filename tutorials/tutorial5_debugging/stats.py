from collections import defaultdict
from typing import Dict, List

from config import PRE_SESSION, POST_SESSION


def index_measurements_by_participant(
    measurements: List[Dict],
) -> Dict[int, Dict[int, float]]:
    """
    Build a nested dict:
        participant_id -> { session -> score }
    """
    index: Dict[int, Dict[int, float]] = defaultdict(dict)

    for rec in measurements:
        pid = rec["participant_id"]
        session = rec["session"]
        score = rec["score"]
        index[pid][session] = score

    return index


def compute_improvements(participants, measurements_index):
    results = []
    for p in participants:
        pid = p["participant_id"]
        name = p["name"]
        group = p["group"]

        participant_measures = measurements_index.get(pid, {})

        if (
            PRE_SESSION not in participant_measures
            or POST_SESSION not in participant_measures
        ):
            continue

        pre_score = participant_measures[PRE_SESSION]
        post_score = participant_measures[POST_SESSION]
        improvement = pre_score - post_score
        if pre_score != 0:
            improvement_index = improvement / pre_score
        else:
            improvement_index = 0.0

        results.append(
            {
                "participant_id": pid,
                "name": name,
                "group": group,
                "pre_score": pre_score,
                "post_score": post_score,
                "improvement": improvement,
                "improvement_index": improvement_index,
            }
        )
    return results


def aggregate_by_group(improvements):
    """
    Aggregate mean pre, post and improvement index per group.

    Returns:
        group -> {
            "count": int,
            "avg_pre": float,
            "avg_post": float,
            "avg_improvement_index": float,
        }
    """
    grouped = {}

    for rec in improvements:
        group = rec["group"]
        if group not in grouped:
            grouped[group] = {
                "count": 0,
                "sum_pre": 0.0,
                "sum_post": 0.0,
                "sum_index": 0.0,
            }

        g = grouped[group]
        g["count"] += 1
        g["sum_pre"] += rec["pre_score"]
        g["sum_post"] += rec["post_score"]
        g["sum_index"] += rec["improvement_index"]

    for group, data in grouped.items():
        count = data["count"] or 1  # avoid division by zero
        data["avg_pre"] = data["sum_pre"] / count
        data["avg_post"] = data["sum_post"] / count
        data["avg_improvement_index"] = data["sum_index"] / count

        # NEW: mean raw change (this will be positive with your CSV)
        data["avg_change"] = data["avg_post"] - data["avg_pre"]

    return grouped
