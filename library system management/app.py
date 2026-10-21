from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            author TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available',
            issued_to TEXT DEFAULT ''
        )
    """)

    columns = [
        row["name"]
        for row in conn.execute("PRAGMA table_info(books)").fetchall()
    ]

    if "status" not in columns:
        conn.execute(
            "ALTER TABLE books ADD COLUMN status TEXT NOT NULL DEFAULT 'Available'"
        )

    if "issued_to" not in columns:
        conn.execute(
            "ALTER TABLE books ADD COLUMN issued_to TEXT DEFAULT ''"
        )

    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = get_db_connection()

    books = conn.execute("SELECT * FROM books").fetchall()

    total_books = len(books)

    available_books = sum(
        1 for book in books
        if book["status"] == "Available"
    )

    issued_books = sum(
        1 for book in books
        if book["status"] == "Issued"
    )

    conn.close()

    return render_template(
        "index.html",
        books=books,
        total_books=total_books,
        available_books=available_books,
        issued_books=issued_books
    )

@app.route("/add", methods=["POST"])
def add_book():
    name = request.form.get("name", "").strip()
    author = request.form.get("author", "").strip()

    if name and author:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO books (name, author) VALUES (?, ?)",
            (name, author)
        )
        conn.commit()
        conn.close()

    return redirect("/")

@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return redirect("/")
@app.route("/issue/<int:book_id>", methods=["POST"])
def issue_book(book_id):
    student_name = request.form.get("student_name", "").strip()

    if not student_name:
        return redirect("/")

    conn = get_db_connection()

    conn.execute("""
        UPDATE books
        SET status = 'Issued', issued_to = ?
        WHERE id = ? AND status = 'Available'
    """, (student_name, book_id))

    conn.commit()
    conn.close()
    return redirect("/")
@app.route("/return/<int:book_id>", methods=["POST"])
def return_book(book_id):
    conn = get_db_connection()

    conn.execute("""
        UPDATE books
        SET status = 'Available', issued_to = ''
        WHERE id = ? AND status = 'Issued'
    """, (book_id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
def return_book(book_id):
    conn = get_db_connection()

    conn.execute("""
        UPDATE books
        SET status = 'Available', issued_to = ''
        WHERE id = ? AND status = 'Issued'
    """, (book_id,))

    conn.commit()
    conn.close()

    return redirect("/")
if __name__ == "__main__":
    create_table()
    app.run(debug=True)