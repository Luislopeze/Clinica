from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
db = SQLAlchemy(app)

# -----------------------------
# MODELOS
# -----------------------------
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    nacimiento = db.Column(db.Date)
    notas = db.Column(db.Text)

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    paciente = db.relationship('Paciente', backref='citas')
    clinica = db.Column(db.String(100))
    fecha = db.Column(db.Date)
    inicio = db.Column(db.Time)
    fin = db.Column(db.Time)
    alumno = db.Column(db.String(100))
    procedimiento = db.Column(db.String(200))
    notas = db.Column(db.Text)

class Historial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente = db.Column(db.String(100))
    clinica = db.Column(db.String(100))
    fecha = db.Column(db.Date)
    horario = db.Column(db.String(50))
    atendido_por = db.Column(db.String(100))
    notas = db.Column(db.Text)

# -----------------------------
# RUTAS
# -----------------------------
@app.route('/')
def inicio():
    pacientes = Paciente.query.all()
    citas = Cita.query.all()
    historial = Historial.query.all()
    clinicas = list(set([c.clinica for c in citas]))
    return render_template('dashboard.html', pacientes=pacientes, citas=citas, historial=historial, clinicas=clinicas)

@app.route('/pacientes')
def pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes.html', pacientes=pacientes)

@app.route('/agenda')
def agenda():
    citas = Cita.query.all()
    return render_template('agenda.html', citas=citas)

@app.route('/historial')
def historial():
    historial = Historial.query.all()
    return render_template('historial.html', historial=historial)

@app.route('/nueva_cita', methods=['GET', 'POST'])
def nueva_cita():
    pacientes = Paciente.query.all()
    if request.method == 'POST':
        paciente_id = request.form['paciente']
        clinica = request.form.get('clinica', 'Clínica Odontológica')
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        inicio = datetime.strptime(request.form['inicio'], '%H:%M').time()
        fin = datetime.strptime(request.form['fin'], '%H:%M').time()
        alumno = request.form['alumno']
        procedimiento = request.form['procedimiento']
        notas = request.form['notas']

        nueva = Cita(
            paciente_id=paciente_id,
            clinica=clinica,
            fecha=fecha,
            inicio=inicio,
            fin=fin,
            alumno=alumno,
            procedimiento=procedimiento,
            notas=notas
        )
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for('agenda'))
    return render_template('nueva_cita.html', pacientes=pacientes)

@app.route('/nuevo_paciente', methods=['GET', 'POST'])
def nuevo_paciente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        nacimiento = datetime.strptime(request.form['nacimiento'], '%Y-%m-%d').date()
        notas = request.form['notas']
        nuevo = Paciente(nombre=nombre, telefono=telefono, nacimiento=nacimiento, notas=notas)
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('pacientes'))
    return render_template('nuevo_paciente.html')

# -----------------------------
# EJECUCIÓN
# -----------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
