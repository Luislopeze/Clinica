from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, date
from modules import db, Paciente, Alumno, Cita

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://elsince:KMKUCB87zO04U3RjqNyz8sSdOxoR70xH@dpg-da8b3q0ae00c73cd5sog-a/clinica_db_ov6b"
app.config['SECRET_KEY'] = "clinica_secret"
db.init_app(app)

# -----------------------------
# RUTAS
# -----------------------------
@app.route("/")
def inicio():
    hoy = date.today().strftime("%Y-%m-%d")
    odontologos = [
        {"nombre": "Luis", "citas": Cita.query.filter_by(atendido_por="Luis", fecha=date.today()).count()},
        {"nombre": "Angie", "citas": Cita.query.filter_by(atendido_por="Angie", fecha=date.today()).count()}
    ]
    citas_hoy = Cita.query.filter_by(fecha=date.today()).all()
    return render_template("inicio.html", hoy=hoy, odontologos=odontologos, citas_hoy=citas_hoy)

@app.route("/dashboard")
def dashboard():
    pacientes = Paciente.query.all()
    citas = Cita.query.all()
    clinicas = list(set([c.clinica for c in citas]))
    # Historial: aquí puedes usar otra tabla o filtrar citas completadas
    historial = []
    return render_template("dashboard.html", pacientes=pacientes, citas=citas, historial=historial, clinicas=clinicas)

@app.route("/pacientes")
def pacientes_view():
    pacientes = Paciente.query.all()
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/nuevo_paciente", methods=["GET", "POST"])
def nuevo_paciente():
    if request.method == "POST":
        folio = "EXP-" + request.form["folio"]
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        nacimiento = datetime.strptime(request.form["nacimiento"], "%Y-%m-%d").date()
        notas = request.form.get("notas", "")
        nuevo = Paciente(folio=folio, nombre=nombre, telefono=telefono,
                         fecha_nacimiento=nacimiento, notas=notas)
        db.session.add(nuevo)
        db.session.commit()
        flash("Paciente registrado correctamente")
        return redirect(url_for("pacientes_view"))
    return render_template("nuevo_paciente.html")

@app.route("/agenda")
def agenda_view():
    citas = Cita.query.all()
    return render_template("agenda.html", citas=citas)

@app.route("/nueva_cita", methods=["GET", "POST"])
def nueva_cita():
    pacientes = Paciente.query.all()
    if request.method == "POST":
        paciente_id = request.form["paciente"]
        clinica = request.form["clinica"]
        horario = request.form["horario"]
        fecha = datetime.strptime(request.form["fecha"], "%Y-%m-%d").date()
        atendido_por = request.form["atendido_por"]
        notas = request.form.get("notas", "")
        nueva = Cita(dia=fecha.strftime("%A"),
                     hora_inicio=horario.split("-")[0],
                     hora_fin=horario.split("-")[1],
                     clinica=clinica,
                     paciente_id=paciente_id,
                     alumno_id=None,
                     notas=notas)
        db.session.add(nueva)
        db.session.commit()
        flash("Cita registrada correctamente")
        return redirect(url_for("agenda_view"))
    return render_template("nueva_cita.html", pacientes=pacientes)

@app.route("/historial")
def historial_view():
    # Aquí puedes implementar un modelo Historial o usar citas con estado
    historial = []
    return render_template("historial.html", historial=historial)

# -----------------------------
# EJECUCIÓN
# -----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
