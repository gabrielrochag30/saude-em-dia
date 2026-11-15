
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("login.html")


@app.route("/pacientes")
def pacientes():
    return render_template("pacientes.html")


@app.route("/visitas")
def visitas():
    return render_template("visitas.html")


if __name__ == "__main__":
    app.run(debug=True)
