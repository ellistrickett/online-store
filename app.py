from flask import Flask
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.db_routes import db_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(db_bp)

if __name__ == "__main__":
    app.run(debug=True)