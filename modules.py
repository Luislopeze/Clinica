from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# -----------------------------
# MODELOS
# -----------------------------

class Paciente(db.Model):
    __tablename__ = "paciente"
    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    notas = db.Column(db.Text)

    def __repr__(self):
        return f"<Paciente {self.nombre}>"


class Alumno(db.Model):
    __tablename__ = "alumno"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"<Alumno {self.nombre}>"


class Cita(db.Model):
    __tablename__ = "cita"
    id = db.Column(db.Integer, primary_key=True)
    dia = db.Column(db.String(20), nullable=False)          # Ejemplo: "Lunes"
    hora_inicio = db.Column(db.String(10), nullable=False)  # Ejemplo: "10:00"
    hora_fin = db.Column(db.String(10), nullable=False)     # Ejemplo: "12:00"
    clinica = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    atendido_por = db.Column(db.String(100))                # Alumno/doctor que atiende
    notas = db.Column(db.Text)

    # Relaciones
    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"))
    alumno_id = db.Column(db.Integer, db.ForeignKey("alumno.id"))

    paciente = db.relationship("Paciente", backref="citas")
    alumno = db.relationship("Alumno", backref="citas")

    def __repr__(self):
        return f"<Cita {self.clinica} {self.fecha}>"
