from fastapi import FastAPI
import sqlite3

app = FastAPI()

DATABASE = "expenses.db"


def create_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)

    connection.commit()
    connection.close()


create_database()


@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}


@app.post("/expenses")
def add_expense(
    category: str,
    amount: float,
    date: str,
    description: str = ""
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (category, amount, date, description)
        VALUES (?, ?, ?, ?)
    """, (category, amount, date, description))

    connection.commit()
    connection.close()

    return {"message": "Expense added successfully"}


@app.get("/expenses")
def get_expenses():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, category, amount, date, description
        FROM expenses
        ORDER BY date DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    expenses = []

    for row in rows:
        expenses.append({
            "id": row[0],
            "category": row[1],
            "amount": row[2],
            "date": row[3],
            "description": row[4]
        })

    return expenses

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()

    connection.close()

    return {"message": "Expense deleted successfully"}