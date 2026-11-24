from flask import Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for('auth.success', name=user))
    return render_template('login.html')

@auth_bp.route('/success/<name>')
def success(name):
    return f"Welcome {name} to the Online Store!"