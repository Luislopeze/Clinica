from flask import Flask, request, render_template, redirect, url_for
from models import db, Paciente, Alumno, Cita

app = Flask(__name__)

# Conexión a tu base de datos en Render
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://clinica_db_ov6b_user:l2yxIhbi371H74I5HVh8B69581fJ1iOI@dpg-da8b3q0ae00c73cd5sog-a/clinica_db_ov6b"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def crear_tablas():
    db.drop_all()   # 🔧 borra todas las tablas viejas
    db.create_all() # 🔧 crea las tablas nuevas según models.py

@app.route("/")
def index():
    return render_template("index.html")

# ---------------- PACIENTES ----------------
@app.route("/formulario")
def formulario():
    return render_template("formulario.html")

@app.route("/paciente", methods=["POST"])
def agregar_paciente():
    numero_folio = request.form["folio"]
    folio_completo = f"EXP-{numero_folio}"

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
@app.route("/formulario_cita")
def formulario_cita():
    pacientes = Paciente.query.all()
    alumnos = Alumno.query.all()
    return render_template("formulario_cita.html", pacientes=pacientes, alumnos=alumnos)

@app.route("/cita", methods=["POST"])
def agregar_cita():
    horario = request.form["horario"]
    partes = horario.split(" ")

    dia = partes[0]
    horas = partes[1]
    hora_inicio, hora_fin = horas.split("-")
    clinica = " ".join(partes[2:])

    nueva_cita = Cita(
        dia=dia,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        clinica=clinica,
        paciente_id=int(request.form["paciente_id"]),
        alumno_id=int(request.form["alumno_id"]),
        notas=request.form.get("notas")
    )
    db.session.add(nueva_cita)
    db.session.commit()
    return redirect(url_for("listar_citas"))

@app.route("/citas")
def listar_citas():
    citas = Cita.query.all()
    return render_template("citas.html", citas=citas)
