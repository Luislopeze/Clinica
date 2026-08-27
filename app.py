from flask import Flask, request, jsonify
from models import db, Paciente

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://clinica_db_ov6b_user:l2yxIhbi371H74I5HVh8B69581fJ1iOI@dpg-da8b3q0ae00c73cd5sog-a/clinica_db_ov6b"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return "Clínica Luis & Angie V2 funcionando 🚀"

# Ruta para registrar un paciente
@app.route("/paciente", methods=["POST"])
def add_paciente():
    data = request.json
    nuevo = Paciente(
        folio=data["folio"],
        nombre=data["nombre"],
        telefono=data.get("telefono"),
        fecha_nacimiento=data.get("fecha_nacimiento"),
        notas=data.get("notas")
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Paciente registrado"}), 201

# Ruta para listar pacientes
@app.route("/pacientes", methods=["GET"])
def listar_pacientes():
    pacientes = Paciente.query.all()
    resultado = [{"folio": p.folio, "nombre": p.nombre, "telefono": p.telefono} for p in pacientes]
    return jsonify(resultado)
