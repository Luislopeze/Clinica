from flask import Flask
from models import db

app = Flask(__name__)

# URL de conexión que Render te dio para tu base PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://clinica_db_ov6b_user:l2yxIhbi371H74I5HVh8B69581fJ1iOI@dpg-da8b3q0ae00c73cd5sog-a/clinica_db_ov6b"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear tablas automáticamente la primera vez que entres
@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return "Clínica Luis & Angie V2 funcionando 🚀"
