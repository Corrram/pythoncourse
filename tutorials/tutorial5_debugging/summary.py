from typing import List, Dict


def format_participant_line(rec: Dict) -> str:
    return (
        f"{rec['participant_id']:>2}  {rec['name']:<6}  "
        f"group: {rec['group']:<9}  "
        f"pre: {rec['pre_score']:>5.1f}  "
        f"post: {rec['post_score']:>5.1f}  "
        f"improvement: {rec['improvement']:>6.1f}"
    )


def generate_report(improvements, group_stats):
    lines = []
    lines.append("Experimental summary")
    lines.append("====================")
    lines.append("")
    lines.append("Group statistics:")
    lines.append("-----------------")
    lines.append("")

    for group, stats in sorted(group_stats.items()):
        lines.append(f"{group} group:")
        lines.append(f" - participants: {stats['count']}")
        lines.append(
            f" - mean raw score: {stats['avg_pre']:.1f} → {stats['avg_post']:.1f}"
        )
        lines.append(f" - mean improvement index: {stats['avg_improvement_index']:.3f}")
        lines.append("")

    # Optional: overall comparison between groups
    if "control" in group_stats and "treatment" in group_stats:
        ctrl = group_stats["control"]
        trt = group_stats["treatment"]
        diff_index = trt["avg_improvement_index"] - ctrl["avg_improvement_index"]

        lines.append("Cohort summary:")
        lines.append("---------------")
        lines.append(
            f"Difference in improvement index (treatment - control): {diff_index:.3f}"
        )

    return "\n".join(lines)
