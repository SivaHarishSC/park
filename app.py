import threading
import subprocess
import sqlite3
import rclpy
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messaging

# Function to get a new SQLite connection
def get_db_connection():
    return sqlite3.connect("data.db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM customer WHERE name=? AND password=?", (name, password))
        data = cur.fetchone()
        con.close()
        if data:
            session['name'] = data[0]
            session['password'] = data[1]
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Username and Password Mismatch', 'danger')
    return redirect(url_for('index'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            password = request.form['password']
            mobile_number = int(request.form['contact'])
            vehicle_id = int(request.form['vehicle_id'])

            con = get_db_connection()
            cur = con.cursor()
            cur.execute(
                "INSERT INTO customer(name, password, mobile_number, vehicle_id) VALUES (?,?,?,?)",
                (name, password, mobile_number, vehicle_id),
            )
            con.commit()
            con.close()
            flash('Record Added Successfully', 'success')
        except Exception as e:
            flash(f"Error in Insert Operation: {str(e)}", 'danger')
        finally:
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/service', methods=['GET', 'POST'])
def service():
    return render_template('service.html')

if __name__ == '__main__':
    app.run(debug=True)
