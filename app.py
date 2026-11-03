from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import get_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', store_status='Online')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('success', name=user))
    return render_template('login.html')

@app.route('/success/<name>')
def success(name):
    return f"Welcome {name} to the Online Store!"

@app.route("/sys-status/db", methods=["GET"])
def check_db_conn():
    """Return information about the current database connection."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Retrieve the database name and user name 
            # for the active connection.
            cur.execute("SELECT current_database(), current_user;")
            database_name, user_name = cur.fetchone()

    return jsonify({
        "database": database_name,
        "user": user_name
    })


if __name__ == '__main__':
    app.run(debug=True)