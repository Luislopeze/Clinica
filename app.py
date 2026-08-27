from flask import Flask
from models import db

app = Flask(__name__)

# Pega aquí la URL que Render te da al crear la base PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://usuario:contraseña@host:puerto/nombre_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def index():
    return "Clínica Luis & Angie V2 funcionando 🚀"
