from flask import Flask, request, render_template, redirect, url_for
from models import db, Paciente, Alumno, Cita

app = Flask(__name__)

# Conexión a tu base PostgreSQL en Render
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

# ---------------- PACIENTES ----------------
@app.route("/formulario")
def formulario():
    return render_template("formulario.html")

@app.route("/paciente", methods=["POST"])
def agregar_paciente():
    numero_folio = request.form["folio"]   # usuario solo escribe el número
    folio_completo = f"EXP-{numero_folio}" # el sistema agrega "EXP-"

    existente = Paciente.query.filter_by(folio=folio_completo).first()
    if existente:
        return render_template("formulario.html", mensaje="⚠️ Ese folio ya existe, usa otro número.")

    nuevo = Paciente(
        folio=folio_completo,
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

# ---------------- ALUMNOS ----------------
@app.route("/formulario_alumno")
def formulario_alumno():
    return render_template("formulario_alumno.html")

@app.route("/alumno", methods=["POST"])
def agregar_alumno():
    matricula = request.form["matricula"]
    existente = Alumno.query.filter_by(matricula=matricula).first()
    if existente:
        return render_template("formulario_alumno.html", mensaje="⚠️ Esa matrícula ya existe, usa otra.")

    nuevo = Alumno(
        nombre=request.form["nombre"],
        matricula=matricula
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for("listar_alumnos"))

@app.route("/alumnos")
def listar_alumnos():
    alumnos = Alumno.query.all()
    return render_template("alumnos.html", alumnos=alumnos)

# ---------------- CITAS ----------------
@app.route("/cita", methods=["POST"])
def agregar_cita():
    # El valor viene como: "Lunes 12:00-14:00 Prótesis Removible"
    horario = request.form["horario"]
    partes = horario.split(" ")

    dia = partes[0]  # Lunes, Martes, etc.
    horas = partes[1]  # "12:00-14:00"
    hora_inicio, hora_fin = horas.split("-")
    clinica = " ".join(partes[2:])  # Prótesis Removible, Clínica Integral, etc.

    nueva_cita = Cita(
        dia=dia,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        clinica=clinica,
        paciente_id=request.form["paciente_id"],
        alumno_id=request.form["alumno_id"],
        notas=request.form.get("notas")
    )
    db.session.add(nueva_cita)
    db.session.commit()
    return redirect(url_for("listar_citas"))

