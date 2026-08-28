from flask import Flask, render_template

app = Flask(__name__)

@app.route("/nueva_cita")
def nueva_cita():
    # Clínicas fijas
    clinicas = ["Clínica Integral", "Prótesis Total", "Prótesis Removible"]

    # Horarios por clínica
    horarios = {
        "Clínica Integral": [
            "Lunes 4pm - 6pm",
            "Martes 4pm - 6pm",
            "Miércoles 10am - 12pm",
            "Jueves 4pm - 6pm",
            "Viernes 10am - 12pm"
        ],
        "Prótesis Total": [
            "Miércoles 4pm - 6pm",
            "Viernes 12pm - 2pm"
        ],
        "Prótesis Removible": [
            "Lunes 12pm - 2pm",
            "Miércoles 12pm - 2pm"
        ]
    }

    pacientes = ["Juan Pérez", "María López", "Carlos Ruiz"]
    return render_template("nueva_cita.html", clinicas=clinicas, horarios=horarios, pacientes=pacientes)
