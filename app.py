from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection details (use environment variables in production)
DB_SERVER = os.getenv('DB_SERVER', 'your-db-server.database.windows.net')
DB_DATABASE = os.getenv('DB_DATABASE', 'your-database-name')
DB_USERNAME = os.getenv('DB_USERNAME', 'your-username')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your-password')

# Create a connection to the SQL database
def get_db_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USERNAME};"
        f"PWD={DB_PASSWORD};"
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']

        try:
            # Insert data into the database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Students (FullName, Email, PhoneNumber, Course) VALUES (?, ?, ?, ?)",
                (full_name, email, phone, course)
            )
            conn.commit()
            cursor.close()
            conn.close()

            flash('Registration successful!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/students')
def students():
    try:
        # Fetch all students from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('students.html', students=students)
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
