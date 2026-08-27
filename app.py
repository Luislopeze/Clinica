from flask import Flask, request, jsonify, render_template
from models import db, Paciente, Alumno, Cita

app = Flask(__name__)

# Conexión a tu base PostgreSQL en Render
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://clinica_db_ov6b_user:l2yxIhbi371H74I5HVh8B69581fJ1iOI@dpg-da8b3q0ae00c73cd5sog-a/clinica_db_ov6b"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear tablas la primera vez que se recibe una petición
@app.before_request
def create_tables_once():
    if not hasattr(app, 'tables_created'):
        db.create_all()
        app.tables_created = True

@app.route("/")
def index():
    return "Clínica Luis & Angie V2 funcionando 🚀"

# Ruta para mostrar el formulario en navegador
@app.route("/formulario")
def formulario():
    return render_template("formulario.html")

# Registrar paciente vía formulario o JSON
@app.route("/paciente", methods=["POST"])
def agregar_paciente():
    # Si viene de formulario HTML
    if request.form:
        nuevo = Paciente(
            folio=request.form["folio"],
            nombre=request.form["nombre"],
            telefono=request.form.get("telefono"),
            fecha_nacimiento=request.form.get("fecha_nacimiento"),
            notas=request.form.get("notas")
        )
    else:  # Si viene en JSON (Postman/cURL)
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

# Listar pacientes
@app.route("/pacientes", methods=["GET"])
def listar_pacientes():
    pacientes = Paciente.query.all()
    resultado = [{"folio": p.folio, "nombre": p.nombre, "telefono": p.telefono} for p in pacientes]
    return jsonify(resultado)
