"""Explore synthetic survey data. Run after pip install -r requirements.txt."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).parent


def analyze(input_path=BASE / 'sample_survey.csv', output_dir=BASE / 'output'):
    df = pd.read_csv(input_path)
    expected = {'study_hours', 'sleep_hours', 'preferred_method'}
    if not expected.issubset(df.columns):
        raise ValueError(f'CSV must include: {sorted(expected)}')
    for col in ['study_hours', 'sleep_hours']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['study_hours', 'sleep_hours', 'preferred_method'])
    df = df[(df.study_hours >= 0) & (df.study_hours <= 24) & (df.sleep_hours >= 0) & (df.sleep_hours <= 24)]
    if df.empty:
        raise ValueError('No valid rows remain')
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = (f'Valid responses: {len(df)}\n'
               f'Average study hours/day: {df.study_hours.mean():.2f}\n'
               f'Average sleep hours/night: {df.sleep_hours.mean():.2f}\n'
               f'Most frequent study method: {df.preferred_method.mode().iloc[0]}\n'
               'Note: Illustrative synthetic responses; no population claims can be made.\n')
    (output_dir / 'summary.txt').write_text(summary, encoding='utf-8')
    df.preferred_method.value_counts().plot.bar(title='Preferred study method')
    plt.ylabel('Responses')
    plt.tight_layout()
    plt.savefig(output_dir / 'study_methods.png')
    plt.close()
    df.plot.scatter(x='sleep_hours', y='study_hours', title='Sleep vs study hours')
    plt.tight_layout()
    plt.savefig(output_dir / 'sleep_study.png')
    plt.close()
    print(summary)
    return summary


if __name__ == '__main__':
    analyze()
