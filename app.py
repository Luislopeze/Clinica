from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, Paciente, Alumno, Cita

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://clinica_db_ov6b_user:l2yxIhbi371H74I5HVh8B69581fJ1iOI@dpg-da8b3q0ae00c73cd5sog-a/clinica_db_ov6b"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_tables_once():
    if not hasattr(app, 'tables_created'):
        db.create_all()
        app.tables_created = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/formulario")
def formulario():
    return render_template("formulario.html")

@app.route("/paciente", methods=["POST"])
def agregar_paciente():
    nuevo = Paciente(
        folio=request.form["folio"],
        nombre=request.form["nombre"],
        telefono=request.form.get("telefono"),
        fecha_nacimiento=request.form.get("fecha_nacimiento"),
        notas=request.form.get("notas")
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for("listar_pacientes"))

@app.route("/pacientes")
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/citas")
def listar_citas():
    citas = Cita.query.all()
    return render_template("citas.html", citas=citas)

