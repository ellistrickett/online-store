<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for

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

if __name__ == '__main__':
=======
from flask import Flask
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.db_routes import db_bp
from routes.user_routes import user_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(db_bp)
app.register_blueprint(user_bp)

if __name__ == "__main__":
    with app.app_context():
        print(app.url_map)
>>>>>>> 049600a6c78e2a1ce0c7ab376afc1a4097bbe36c
    app.run(debug=True)