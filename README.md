# Coding & Quant Engineering Portfolio

Python and SQL projects exploring data engineering, quantitative finance, and practical problem-solving.

This portfolio brings together two introductory quant projects and four smaller programming exercises. My interests include working with datasets, building reliable tools, and understanding how code can support financial research.

## Quant engineering projects

| Project | Technologies | Focus |
| --- | --- | --- |
| [Financial Data Pipeline](financial-data-pipeline/) | Python, pandas, SQLite | Validates price records, stores them in a database, and calculates daily returns. |
| [Moving-Average Backtester](quant-backtester/) | Python, pandas, Matplotlib | Tests a simple trend-following signal and compares simulated results with buy-and-hold. |

Both projects include reproducible sample data, setup instructions, and automated tests. The pipeline also supports optional historical data retrieval.

## Other programming projects

| Project | Technologies | Focus |
| --- | --- | --- |
| [Grade Tracker](grade-tracker/) | Python | Weighted grade calculations |
| [Study Habits Analysis](study-survey/) | Python, pandas, Matplotlib | Data cleaning and visualization |
| [Library Database](library-sql/) | SQL, SQLite | Relational databases and queries |
| [Expense Dashboard](expense-dashboard/) | Python, Matplotlib | Budget summaries and charts |

## Relevant experience

- **AI and machine learning:** Built an image-recognition model with an NVIDIA Jetson Nano as part of a hands-on AI program.
- **Data engineering internship:** Worked with SQL queries and database analysis for school information systems at Green Moons Company Limited.

These experiences are described here for context; supporting certificates and the original AI project are maintained separately from the code in this repository.

## Repository organization

- [`main`](../../tree/main): all six projects
- [`quant-projects`](../../tree/quant-projects): financial data pipeline and backtester
- [`coding-projects`](../../tree/coding-projects): four introductory coding projects

Each project folder has its own README with instructions. To run the available tests from the repository root:

```bash
python -m pip install "pandas>=2.0,<3" "matplotlib>=3.7,<4"
python -m unittest discover -s tests -v
python -m unittest discover -s financial-data-pipeline/tests -v
python -m unittest discover -s quant-backtester/tests -v
```

## Notes

The code in this repository consists of **AI-assisted learning and demonstration projects**. The example datasets are fictional, and the backtester is for educational analysis rather than live trading. I plan to extend these projects through hands-on experimentation and documented changes.

[MIT License](LICENSE)
