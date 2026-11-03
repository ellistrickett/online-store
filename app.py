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
    app.run(debug=True)