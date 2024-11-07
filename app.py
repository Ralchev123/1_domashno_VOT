from flask import Flask, render_template, request, redirect
import psycopg2
import os
from dotenv import load_dotenv  
import time

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn

def create_table_if_not_exists():
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            position VARCHAR(100),
            salary DECIMAL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


create_table_if_not_exists()
time.sleep(2)

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']  
        position = request.form['position'] 
        salary = request.form['salary'] 

        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s)", (name, position, salary))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/')

@app.route('/update_salary/<int:id>', methods=['GET', 'POST'])
def update_salary(id):
    if request.method == 'POST':
        new_salary = request.form['salary']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE employees SET salary = %s WHERE id = %s", (new_salary, id))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE id = %s", (id,))
    employee = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('update_salary.html', employee=employee)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
