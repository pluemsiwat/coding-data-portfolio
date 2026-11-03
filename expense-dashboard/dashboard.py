"""Create a simple monthly dashboard using fictional expenses."""
import csv
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = Path(__file__).parent


def summarize(path=BASE / 'sample_expenses.csv', budget_path=BASE / 'sample_budgets.csv', output=BASE / 'output'):
    totals = defaultdict(float)
    with open(path, newline='', encoding='utf-8') as file:
        for row in csv.DictReader(file):
            amount = float(row['amount_thb'])
            if amount < 0:
                raise ValueError('Expense amount cannot be negative')
            totals[row['category']] += amount
    budgets = {}
    with open(budget_path, newline='', encoding='utf-8') as file:
        for row in csv.DictReader(file):
            budgets[row['category']] = float(row['budget_thb'])
    categories = sorted(set(totals) | set(budgets))
    if not categories:
        raise ValueError('No budget or expense data found')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    with open(output / 'budget_comparison.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['category', 'budget_thb', 'actual_thb', 'remaining_thb'])
        for category in categories:
            writer.writerow([category, f'{budgets.get(category,0):.2f}', f'{totals.get(category,0):.2f}', f'{budgets.get(category,0)-totals.get(category,0):.2f}'])
    x = range(len(categories))
    plt.figure(figsize=(9, 5))
    plt.bar([n - .2 for n in x], [budgets.get(c,0) for c in categories], width=.4, label='Budget')
    plt.bar([n + .2 for n in x], [totals.get(c,0) for c in categories], width=.4, label='Actual')
    plt.xticks(list(x), categories, rotation=20)
    plt.ylabel('THB')
    plt.title('Monthly expenses: budget vs actual')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output / 'dashboard.png')
    plt.close()
    total = sum(totals.values())
    print(f'Total sample expenses: {total:,.2f} THB')
    print(f'Files saved in {output}')
    return total


if __name__ == '__main__':
    summarize()
