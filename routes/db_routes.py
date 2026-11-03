from flask import Blueprint, jsonify
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
