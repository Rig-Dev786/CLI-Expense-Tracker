# CLI Expense Tracker & Analyser

#### Video Demo: https://www.youtube.com/watch?v=gO2aB9MwE0A

#### Description:A Command-Line Expense Tracker and Analyser, a daily-use application right into your terminal for managing your daily expenses in a database.

A command-line expense tracking application built in Python that allows users
to manage their daily expenses efficiently. The project uses SQLite as its
database engine, matplotlib for data visualization, and pytest for testing.

## Features

- **Add Expenses** — Log an expense with description, amount, and category
- **List Expenses** — View all expenses in a formatted table
- **Summary** — View total spending grouped by category
- **Delete Expenses** — Remove an expense by ID
- **Visual Dashboard** — Generate a 4-panel matplotlib chart saved as PNG
- **Save Report** — Export all transactions to a formatted `.txt` file

## Project Files

### `project.py`
The main application file containing all core logic. It includes:
- `main()` — Entry point, handles CLI commands via `sys.argv`
- `init_db()` — Initializes the SQLite database and creates the expenses table if it doesn't exist
- `add_expense()` — Inserts a new expense record into the database with validation
- `list_expenses()` — Fetches and displays all expenses in a tabular format
- `delete_expense()` — Deletes a record by ID and raises ValueError if not found
- `print_summary()` — Aggregates and displays total spending by category
- `plot_expenses()` — Generates a 4-panel dashboard (bar, pie, line, horizontal bar) saved as PNG
- `save_report()` — Exports all transactions to a `.txt` file

### `test_project.py`
Contains 9 pytest tests covering all major functions. Each test uses a
`setup_db` fixture that wipes the database clean before every test run,
ensuring full isolation and reproducibility.

### `requirements.txt`
Lists all pip dependencies:
- `pytest` — for running tests
- `matplotlib` — for generating expense visualizations

## Design Choices

**Why SQLite over a plain CSV file?**
SQLite allows proper relational data storage, enforces constraints like
`CHECK(amount > 0)` at the database level, and makes aggregation queries
trivial. It also serves as a foundation for the larger PostgreSQL-based
full-stack project this CLI will eventually power.

**Why raw SQL over an ORM?**
Using raw SQL via Python's built-in `sqlite3` module keeps the project
lightweight and makes the database logic explicit and educational — which
aligns with the academic goals of this project.

**Why matplotlib over a web-based chart?**
Since this is a CLI tool, matplotlib was the most natural fit. The dashboard
saves as a PNG file making it portable and viewable anywhere without needing
a browser or server.



## How to Run

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Commands
python project.py add
python project.py list
python project.py summary
python project.py delete
python project.py plot
python project.py report

# Tests
pytest test_project.py -v


## Future Scope

This CLI project is the foundation of a larger full-stack expense splitting
application (like Splitwise) that will use PostgreSQL, Node.js, and React -
implementing advanced DBMS concepts like ACID transactions, triggers, stored
procedures, and a graph-based debt settlement algorithm.
