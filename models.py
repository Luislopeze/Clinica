from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    folio = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    notas = db.Column(db.Text)

class Alumno(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)  # encriptada

class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    folio_paciente = db.Column(db.String(20), db.ForeignKey('pacientes.folio', ondelete="CASCADE"))
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id', ondelete="CASCADE"))
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    procedimiento = db.Column(db.String(50))
    estado = db.Column(db.String(20), default='Programada')
    notas = db.Column(db.Text)

    __table_args__ = (db.UniqueConstraint('alumno_id', 'fecha', 'hora', name='unique_cita'),)
