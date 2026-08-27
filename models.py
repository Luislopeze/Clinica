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
    dia = db.Column(db.String(20), nullable=False)       # Ejemplo: "Lunes"
    hora_inicio = db.Column(db.String(10), nullable=False)  # Ejemplo: "12:00"
    hora_fin = db.Column(db.String(10), nullable=False)     # Ejemplo: "14:00"
    clinica = db.Column(db.String(50), nullable=False)   # Ejemplo: "Prótesis Removible"
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'))
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumno.id'))
    notas = db.Column(db.Text)

