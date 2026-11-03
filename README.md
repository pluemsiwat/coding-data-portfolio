# Coding & Quantitative Engineering Portfolio

A collection of small, practical projects using Python, SQL, and data analysis tools. The projects cover general programming foundations and introductory quantitative finance engineering.

## Quantitative finance and engineering

| Project | Tools | Overview |
| --- | --- | --- |
| [Financial Data Pipeline](financial-data-pipeline/) | Python, pandas, SQLite | Validates daily market-price data, stores it in SQLite, and calculates returns. |
| [Moving-Average Strategy Backtester](quant-backtester/) | Python, pandas, Matplotlib | Tests a basic trading signal and compares simulated performance with a buy-and-hold benchmark. |

## Other coding and data projects

| Project | Tools | Overview |
| --- | --- | --- |
| [Student Grade Tracker](grade-tracker/) | Python | Calculates weighted assignment averages and summarizes results. |
| [Study Habits Analysis](study-survey/) | Python, pandas, Matplotlib | Cleans fictional survey data and generates descriptive charts. |
| [Library Database](library-sql/) | SQL, SQLite | Models borrowing records and explores data with SQL queries. |
| [Expense Dashboard](expense-dashboard/) | Python, Matplotlib | Compares sample monthly expenses with category budgets. |

## Browse by category

- [Coding projects branch](https://github.com/pluemsiwat/coding-data-portfolio/tree/coding-projects): the four introductory coding/data projects
- [Quant projects branch](https://github.com/pluemsiwat/coding-data-portfolio/tree/quant-projects): the financial data pipeline and strategy backtester
- **Main branch (this page):** all six projects together

These branches are alternate collections for browsing. Each project also has its own folder so you don't need to switch branches to explore everything.

## How to run the projects

Each folder contains a README with setup instructions, dependencies, and sample usage. Python 3.10+ is recommended for the quant projects. Run the projects' automated checks using:

```bash
python -m pip install "pandas>=2.0,<3" "matplotlib>=3.7,<4"
python -m unittest discover -s tests -v
python -m unittest discover -s financial-data-pipeline/tests -v
python -m unittest discover -s quant-backtester/tests -v
```

## Project notes

These are **AI-assisted demonstration projects** made for practice and further development, not a record of independently written past work. Data in the included demos is fictional. Historical market-data import is optional in the pipeline, and the strategy backtest is for educational research, not investment advice.

Related experience, documented separately: an NVIDIA Jetson Nano object-recognition project and a data-engineering internship involving SQL and school information systems.

Licensed under the [MIT License](LICENSE).
