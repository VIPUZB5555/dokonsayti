from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def init_db():
    if not os.path.exists("database.db"):
        conn = sqlite3.connect("database.db")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL
            );
        """)
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template("index.html", products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        conn = sqlite3.connect("database.db")
        conn.execute("INSERT INTO products (name, quantity) VALUES (?, ?)", (name, quantity))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template("add.html")

@app.route('/sell/<int:product_id>')
def sell_product(product_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
    result = cursor.fetchone()
    if result and result[0] > 0:
        cursor.execute("UPDATE products SET quantity = quantity - 1 WHERE id = ?", (product_id,))
        conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
