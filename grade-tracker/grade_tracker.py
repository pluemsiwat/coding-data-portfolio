"""Simple weighted-grade tracker. Run: python grade_tracker.py"""
from dataclasses import dataclass


@dataclass
class Assignment:
    name: str
    score: float
    maximum: float
    weight: float

    def __post_init__(self):
        if self.maximum <= 0 or not 0 <= self.score <= self.maximum:
            raise ValueError('Score must be between 0 and a positive maximum')
        if self.weight <= 0:
            raise ValueError('Weight must be positive')


def weighted_average(assignments):
    if not assignments:
        raise ValueError('Add at least one assignment')
    total_weight = sum(a.weight for a in assignments)
    return sum((a.score / a.maximum) * a.weight for a in assignments) / total_weight * 100


def main():
    print('Grade Tracker | enter blank subject to finish')
    subjects = {}
    while True:
        subject = input('Subject: ').strip()
        if not subject:
            break
        name = input('Assignment name: ').strip() or 'Assignment'
        try:
            score = float(input('Points earned: '))
            maximum = float(input('Points possible: '))
            weight = float(input('Relative weight (e.g. 20): '))
            assignment = Assignment(name, score, maximum, weight)
        except ValueError as exc:
            print(f'Invalid entry: {exc}. Try again.')
            continue
        subjects.setdefault(subject, []).append(assignment)
        print(f'{subject}: {weighted_average(subjects[subject]):.1f}% so far')
    print('\nSummary')
    for subject, assignments in subjects.items():
        print(f'{subject}: {weighted_average(assignments):.1f}% ({len(assignments)} entries)')
    if not subjects:
        print('No assignments entered.')


if __name__ == '__main__':
    main()
