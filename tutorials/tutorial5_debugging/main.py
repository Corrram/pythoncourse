from loader import load_participants, load_measurements
from preprocessing import clean_participants, clean_measurements
from stats import index_measurements_by_participant, compute_improvements, aggregate_by_group
from summary import generate_report


def main():
    participants_raw = load_participants("data/participants.csv")
    measurements_raw = load_measurements("data/measurements.csv")

    participants = clean_participants(participants_raw)
    measurements = clean_measurements(measurements_raw)

    index = index_measurements_by_participant(measurements)
    improvements = compute_improvements(participants, index)
    group_stats = aggregate_by_group(improvements)

    report = generate_report(improvements, group_stats)
    print(report)


if __name__ == "__main__":
    main()
