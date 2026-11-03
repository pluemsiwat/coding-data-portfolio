import importlib.util
from pathlib import Path
import sqlite3
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    import sys
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class PortfolioTests(unittest.TestCase):
    def test_grade_average(self):
        grade = load('grade_tracker', 'grade-tracker/grade_tracker.py')
        entries = [grade.Assignment('Quiz', 8, 10, 20), grade.Assignment('Exam', 90, 100, 80)]
        self.assertAlmostEqual(grade.weighted_average(entries), 88)
        with self.assertRaises(ValueError):
            grade.Assignment('Wrong', 11, 10, 20)

    def test_library_queries(self):
        db = sqlite3.connect(':memory:')
        sql = (ROOT / 'library-sql/library.sql').read_text()
        db.executescript(sql)
        self.assertEqual(db.execute('SELECT COUNT(*) FROM loans').fetchone()[0], 5)
        self.assertEqual(db.execute('SELECT COUNT(*) FROM loans WHERE returned_on IS NULL').fetchone()[0], 3)
        db.close()

    def test_expenses(self):
        dashboard = load('dashboard', 'expense-dashboard/dashboard.py')
        with tempfile.TemporaryDirectory() as tmp:
            total = dashboard.summarize(output=Path(tmp))
            self.assertAlmostEqual(total, 1325)
            self.assertTrue((Path(tmp) / 'dashboard.png').exists())
            self.assertTrue((Path(tmp) / 'budget_comparison.csv').exists())

    def test_survey(self):
        survey = load('survey_analysis', 'study-survey/survey_analysis.py')
        with tempfile.TemporaryDirectory() as tmp:
            result = survey.analyze(output_dir=Path(tmp))
            self.assertIn('Valid responses: 12', result)
            self.assertTrue((Path(tmp) / 'study_methods.png').exists())
            self.assertTrue((Path(tmp) / 'sleep_study.png').exists())


if __name__ == '__main__':
    unittest.main()
