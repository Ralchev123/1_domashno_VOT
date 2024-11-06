from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(dbname="votdatabase", user="ralchev", password="nikola12!", host="localhost")
    return conn

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
        name = request.form['name']  # Corrected from request.fo
        position = request.form['position']  # Corrected from request.fo
        salary = request.form['salary']  # Corrected from request.fo

        # Insert the data into the database
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
    app.run(debug=True)
