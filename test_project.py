import pytest
import sqlite3
import os
from project import add_expense, delete_expense, list_expenses, print_summary, init_db, save_report, plot_expenses

DB_NAME = "expenses.db"

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    conn.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()
    yield

def test_add_expense():
    add_expense("Lunch", 150.0, "food")
    conn = sqlite3.connect(DB_NAME)
    row = conn.execute("SELECT * FROM expenses WHERE description = 'Lunch'").fetchone()
    conn.close()
    assert row is not None
    assert row[2] == 150.0
    assert row[3] == "food"

def test_add_expense_invalid_amount():
    with pytest.raises(ValueError):
        add_expense("Invalid", -50, "food")

def test_delete_expense():
    add_expense("Coffee", 80.0, "food")
    conn = sqlite3.connect(DB_NAME)
    exp_id = conn.execute("SELECT id FROM expenses WHERE description = 'Coffee'").fetchone()[0]
    conn.close()
    delete_expense(exp_id)
    conn = sqlite3.connect(DB_NAME)
    row = conn.execute("SELECT * FROM expenses WHERE id = ?", (exp_id,)).fetchone()
    conn.close()
    assert row is None

def test_delete_nonexistent_expense():
    with pytest.raises(ValueError):
        delete_expense(99999)

def test_summary_returns_categories():
    add_expense("Rent", 5000.0, "rent")
    add_expense("Bus", 200.0, "travel")
    rows = print_summary()
    categories = [r[0] for r in rows]
    assert "rent" in categories
    assert "travel" in categories

def test_list_expenses_returns_all():
    add_expense("Pizza", 300.0, "food")
    add_expense("Hotel", 2000.0, "travel")
    rows = list_expenses()
    assert len(rows) == 2

def test_save_report_creates_file():
    add_expense("Test", 100.0, "misc")
    filename = save_report("test_report.txt")
    assert os.path.exists("test_report.txt")
    os.remove("test_report.txt")

def test_save_report_contains_total():
    add_expense("Groceries", 500.0, "food")
    save_report("test_report.txt")
    with open("test_report.txt") as f:
        content = f.read()
    assert "TOTAL" in content
    assert "500.00" in content
    os.remove("test_report.txt")

def test_plot_expenses_no_crash():
    add_expense("Travel", 300.0, "travel")
    try:
        plot_expenses()
    except Exception as e:
        pytest.fail(f"plot_expenses() raised an exception: {e}")
