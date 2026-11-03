from flask import Blueprint, jsonify, render_template, request
from db import get_connection

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route("/html-register", methods=["GET", "POST"])
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

@user_bp.route("/", methods=["GET"])
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

@user_bp.route("/<int:user_id>", methods=["GET"])
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

@user_bp.route("/<int:user_id>/update", methods=["GET", "PUT"])
def update_user_by_id(user_id):
    """Display or update a user's details by ID."""
    if request.method == "GET":
        stmt = "SELECT user_id, email, password_hash, first_name, last_name FROM users WHERE user_id = %s;"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(stmt, (user_id,))
                row = cur.fetchone()

        if row is None:
            return "User not found", 404

        user = {
            "user_id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "first_name": row[3],
            "last_name": row[4]
        }

        return render_template("user-update.html", user=user)

    # Handle PUT request
    data = request.get_json()
    new_email = data.get("email")
    new_password = data.get("password_hash")
    new_first = data.get("first_name")
    new_last = data.get("last_name")

    if not all([new_email, new_password, new_first, new_last]):
        return jsonify({
            "message": "Email, password_hash, first_name, and last_name are all required."
        }), 400

    stmt = """
        UPDATE users
        SET email = %s, password_hash = %s, first_name = %s, last_name = %s
        WHERE user_id = %s
        RETURNING user_id, email, first_name, last_name;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(stmt, (new_email, new_password, new_first, new_last, user_id))
            row = cur.fetchone()
        conn.commit()

    if row is None:
        return jsonify({
            "message": "No user found or updated."
        }), 404

    updated_user = {
        "user_id": row[0],
        "email": row[1],
        "first_name": row[2],
        "last_name": row[3]
    }

    return jsonify(updated_user), 200

@user_bp.route("/<int:user_id>/delete", methods=["GET"])
def delete_user_page(user_id):
    """Display the delete confirmation page for a user (Section L)."""
    stmt = """
        SELECT user_id, email, password_hash, first_name, last_name 
        FROM users 
        WHERE user_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(stmt, (user_id,))
            row = cur.fetchone()

    if row is None:
        return "User not found", 404

    user = {
        "user_id": row[0],
        "email": row[1],
        "password_hash": row[2],
        "first_name": row[3],
        "last_name": row[4]
    }

    return render_template("user-delete.html", user=user)


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user record from the database by ID using the DELETE method (Section M)."""
    stmt = """
        DELETE FROM users 
        WHERE user_id = %s 
        RETURNING user_id, email;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(stmt, (user_id,))
            row = cur.fetchone()
        conn.commit()

    if row is None:
        return jsonify({
            "message": "User not found."
        }), 404

    return jsonify({
        "message": "The user has been deleted.",
        "user_id": row[0],
        "email": row[1]
    }), 200