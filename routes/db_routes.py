from flask import Blueprint, jsonify, request, render_template
from db import get_connection
from models import create_tables

db_bp = Blueprint('database', __name__)

@db_bp.route("/sys-status/db", methods=["GET"])
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

@db_bp.route("/db/init", methods=["GET"])
def init_db():
    """Route to trigger PostgreSQL DDL initialization."""
    create_tables()
    return "PostgreSQL database tables (users, orders, order_items) have been created successfully."

@db_bp.route("/users/html-register", methods=["GET", "POST"])
def register_user_bypost():
    """Display the HTML form or insert a new user record into the database via POST."""
    if request.method == "GET":
        return render_template("register-user.html")

    email = request.form.get("email")
    password_hash = request.form.get("password_hash")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")

    if not all([email, password_hash, first_name, last_name]):
        return jsonify({
            "error": "email, password_hash, first_name, and last_name are required."
        }), 400

    stmt = """
        INSERT INTO users (email, password_hash, first_name, last_name)
        VALUES (%s, %s, %s, %s)
        RETURNING user_id;
    """

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(stmt, (email, password_hash, first_name, last_name))
                new_id = cur.fetchone()[0]
            conn.commit()

        return jsonify({
            "query result": "The user has been registered.",
            "user_id": new_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@db_bp.route("/users", methods=["GET"])
def get_users():
    """Retrieve all user records from the PostgreSQL users table."""
    stmt = """
        SELECT user_id, email, password_hash, first_name, last_name, created_at
        FROM users
        ORDER BY user_id;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(stmt)
            rows = cur.fetchall()

    if not rows:
        return jsonify({"query result": "No users found"}), 404

    users = []
    for row in rows:
        users.append({
            "user_id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "first_name": row[3],
            "last_name": row[4],
            "created_at": row[5]
        })

    return jsonify(users), 200

@db_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """Get a user record from the database by ID in a RESTful way."""
    stmt = """
        SELECT user_id, email, password_hash, first_name, last_name, created_at
        FROM users
        WHERE user_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(stmt, (user_id,))
            row = cur.fetchone()

    if row is None:
        return jsonify({
            "query result": "No user found"
        }), 404

    user = {
        "user_id": row[0],
        "email": row[1],
        "password_hash": row[2],
        "first_name": row[3],
        "last_name": row[4],
        "created_at": row[5]
    }

    return jsonify(user), 200