from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    notas = db.Column(db.Text)

class Alumno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(50), unique=True, nullable=False)

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    notas = db.Column(db.Text)
