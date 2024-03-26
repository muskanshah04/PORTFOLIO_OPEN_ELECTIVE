from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
@app.route('/')
def portfolio():
   return
render_template('portfolio.html')

@app.route('/profile')
def profile():
   return
render_template('profile.html')

@app.route('/edu')
def edu():
   return
render_template('edu.html')

@app.route('/exp')
def exp():
   return
render_template('exp.html')

@app.route('/skills')
def skills():
   return
render_template('skills.html')


# Function to create a connection to SQLite database
def get_db_connection():
    conn = sqlite3.connect('trip_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize database
def initialize_database():
    try:
        conn = get_db_connection()
        conn.execute('CREATE TABLE IF NOT EXISTS trips (id INTEGER PRIMARY KEY, source TEXT, destination TEXT, start_date TEXT, end_date TEXT, num_travelers INTEGER, expense REAL, mode_of_payment TEXT)')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {str(e)}")

# Check if database file exists, if not, create it
initialize_database()

@app.route('/')
def profile():
    return render_template('profile.html')

@app.route('/submit', methods=['POST'])
def add_trip():
    if request.method == 'POST':
        # Retrieve form data
        source = request.form['source']
        destination = request.form['destination']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        num_travelers = request.form['num_travelers']
        expense = request.form['expense']
        mode_of_payment = request.form['mode_of_payment']

        try:
            # Store trip data in the database
            conn = get_db_connection()
            conn.execute("INSERT INTO trips (source, destination, start_date, end_date, num_travelers, expense, mode_of_payment) VALUES (?, ?, ?, ?, ?, ?, ?)", (source, destination, start_date, end_date, num_travelers, expense, mode_of_payment))
            conn.commit()
            conn.close()
            return redirect(url_for('profile'))
        except Exception as e:
            print(f"Error adding trip: {str(e)}")
            return 'Error adding trip'

@app.route('/remove/<int:trip_id>', methods=['POST'])
def remove_trip(trip_id):
    if request.method == 'POST':
        try:
            # Remove trip from the database
            conn = get_db_connection()
            conn.execute('DELETE FROM trips WHERE id = ?', (trip_id,))
            conn.commit()
            conn.close()
            return redirect(url_for('profile'))
        except Exception as e:
            print(f"Error removing trip: {str(e)}")
            return 'Error removing trip'
@app.route('/summary')
def summary():
    # Fetch trip data from the database
    conn = get_db_connection()
    trips = conn.execute('SELECT * FROM trips').fetchall()
    conn.close()
    return render_template('summary.html', trips=trips)



if__name__=='__main__':
app.run(debug=True)
