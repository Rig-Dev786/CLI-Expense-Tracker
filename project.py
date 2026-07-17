import sqlite3
import sys
from datetime import date

DB_NAME = "expenses.db"

def main():
    init_db()
    if len(sys.argv) < 2:
        print("Usage: python project.py [add|list|summary|delete|plot|report]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "add":
        desc = input("Description: ")
        amount = float(input("Amount: "))
        category = input("Category (food/travel/rent/misc): ")
        add_expense(desc, amount, category)
    elif command == "list":
        list_expenses()
    elif command == "summary":
        print_summary()
    elif command == "delete":
        list_expenses()
        exp_id = int(input("Enter ID to delete: "))
        delete_expense(exp_id)
    elif command == "plot":
        plot_expenses()
    elif command == "report":
        save_report()
    else:
        print("Unknown command.")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_expense(description, amount, category):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    conn = sqlite3.connect(DB_NAME)
    conn.execute(
        "INSERT INTO expenses (description, amount, category, date) VALUES (?, ?, ?, ?)",
        (description, amount, category, str(date.today()))
    )
    conn.commit()
    conn.close()
    print(f"Added: {description} ₹{amount:.2f} [{category}]")

def list_expenses():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    conn.close()
    if not rows:
        print("No expenses found.")
        return rows
    print(f"\n{'ID':<5} {'Date':<12} {'Category':<10} {'Amount':>10}  Description")
    print("-" * 55)
    for row in rows:
        print(f"{row[0]:<5} {row[3]:<12} {row[4]:<10} ₹{row[2]:>8.2f}  {row[1]}")
    return rows

def delete_expense(exp_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise ValueError(f"No expense found with ID {exp_id}")
    print(f"Deleted expense ID {exp_id}")

def print_summary():
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category"
    ).fetchall()
    total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0
    conn.close()
    print("\nSummary by Category:")
    print("-" * 30)
    for row in rows:
        print(f"  {row[0]:<12} ₹{row[1]:>8.2f}")
    print("-" * 30)
    print(f"  {'TOTAL':<12} ₹{total:>8.2f}\n")
    return rows

def plot_expenses():
    import matplotlib.pyplot as plt
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("SELECT * FROM expenses ORDER BY date ASC").fetchall()
    conn.close()

    if not rows:
        print("No expenses to plot.")
        return

    #Data
    ids =          [r[0] for r in rows]
    descriptions = [r[1] for r in rows]
    amounts =      [r[2] for r in rows]
    categories =   [r[3] for r in rows]
    dates =        [r[4] for r in rows]

    #Category
    cat_totals = {}
    for cat, amt in zip(categories, amounts):
        cat_totals[cat] = cat_totals.get(cat, 0) + amt

    # Aggregate by date
    date_totals = {}
    for d, amt in zip(dates, amounts):
        date_totals[d] = date_totals.get(d, 0) + amt

    # Top 5 expenses
    sorted_expenses = sorted(zip(amounts, descriptions), reverse=True)[:5]
    top_amounts = [x[0] for x in sorted_expenses]
    top_labels =  [x[1][:15] for x in sorted_expenses]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Expense Dashboard", fontsize=16, fontweight="bold")

    axes[0, 0].bar(cat_totals.keys(), cat_totals.values(), color="steelblue")
    axes[0, 0].set_title("Total by Category")
    axes[0, 0].set_xlabel("Category")
    axes[0, 0].set_ylabel("Amount (₹)")

    # 2.Pie chart
    axes[0, 1].pie(
        cat_totals.values(),
        labels=cat_totals.keys(),
        autopct="%1.1f%%",
        startangle=140
    )
    axes[0, 1].set_title("Category Distribution")

    # 3. Line chart. time
    axes[1, 0].plot(
        list(date_totals.keys()),
        list(date_totals.values()),
        marker="o", color="darkorange", linewidth=2
    )
    axes[1, 0].set_title("Spending Over Time")
    axes[1, 0].set_xlabel("Date")
    axes[1, 0].set_ylabel("Amount (₹)")
    axes[1, 0].tick_params(axis="x", rotation=45)

    # 4. Horizontal bar. top 5 expenses
    axes[1, 1].barh(top_labels, top_amounts, color="mediumseagreen")
    axes[1, 1].set_title("Top Expenses")
    axes[1, 1].set_xlabel("Amount (₹)")

    plt.tight_layout()
    plt.savefig("expenses_chart.png", dpi=150)
    plt.close()
    print("Dashboard saved as expenses_chart.png")

def save_report(filename="report.txt"):
    conn = sqlite3.connect(DB_NAME)
    rows = conn.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0] or 0
    conn.close()
    with open(filename, "w") as f:
        f.write("EXPENSE REPORT\n")
        f.write("=" * 55 + "\n")
        f.write(f"{'ID':<5} {'Date':<12} {'Category':<10} {'Amount':>10}  Description\n")
        f.write("-" * 55 + "\n")
        for row in rows:
            f.write(f"{row[0]:<5} {row[3]:<12} {row[4]:<10} ₹{row[2]:>8.2f}  {row[1]}\n")
        f.write("=" * 55 + "\n")
        f.write(f"TOTAL: ₹{total:.2f}\n")
    print(f"Report saved as {filename}")
    return filename

if __name__ == "__main__":
    main()
