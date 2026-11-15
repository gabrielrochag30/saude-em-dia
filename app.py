
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

from database import get_connection

app = Flask(__name__)


def listar_pacientes(busca=""):
    connection = get_connection()

    try:
        if busca:
            pacientes = connection.execute(
                """
                SELECT * FROM pacientes
                WHERE ativo = 1 AND nome LIKE ?
                ORDER BY nome
                """,
                (f"%{busca}%",)
            ).fetchall()
        else:
            pacientes = connection.execute(
                """
                SELECT * FROM pacientes
                WHERE ativo = 1
                ORDER BY nome
                """
            ).fetchall()

        return pacientes

    finally:
        connection.close()


def obter_paciente(id_paciente):
    connection = get_connection()

    try:
        return connection.execute(
            "SELECT * FROM pacientes WHERE id_paciente = ?",
            (id_paciente,)
        ).fetchone()

    finally:
        connection.close()


@app.template_filter("data_br")
def data_br(data):
    if not data:
        return ""

    return datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")


@app.route("/")
def inicio():
    return render_template("login.html")


@app.route("/pacientes", methods=["GET", "POST"])
def pacientes():
    if request.method == "POST":
        id_paciente = request.form.get("id_paciente", "").strip()
        nome = request.form.get("nome", "").strip()
        nascimento = request.form.get("nascimento", "").strip()
        endereco = request.form.get("endereco", "").strip()
        telefone = request.form.get("telefone", "").strip()
        cadastro = request.form.get("cadastro", "").strip()

        paciente_edicao = {
            "id_paciente": id_paciente,
            "nome": nome,
            "data_nascimento": nascimento,
            "endereco": endereco,
            "telefone": telefone,
            "numero_cadastro": cadastro
        }

        if not nome or not endereco:
            return render_template(
                "pacientes.html",
                pacientes=listar_pacientes(),
                paciente_edicao=paciente_edicao,
                busca="",
                mensagem="Preencha os campos obrigatórios."
            )

        if nascimento:
            try:
                datetime.strptime(nascimento, "%Y-%m-%d")
            except ValueError:
                return render_template(
                    "pacientes.html",
                    pacientes=listar_pacientes(),
                    paciente_edicao=paciente_edicao,
                    busca="",
                    mensagem="Informe uma data de nascimento válida."
                )

        connection = get_connection()

        try:
            if id_paciente:
                connection.execute(
                    """
                    UPDATE pacientes
                    SET nome = ?, data_nascimento = ?, endereco = ?,
                        telefone = ?, numero_cadastro = ?
                    WHERE id_paciente = ?
                    """,
                    (
                        nome,
                        nascimento or None,
                        endereco,
                        telefone or None,
                        cadastro or None,
                        id_paciente
                    )
                )
                mensagem = "Paciente atualizado com sucesso!"

            else:
                connection.execute(
                    """
                    INSERT INTO pacientes
                    (nome, data_nascimento, endereco, telefone, numero_cadastro)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        nome,
                        nascimento or None,
                        endereco,
                        telefone or None,
                        cadastro or None
                    )
                )
                mensagem = "Paciente cadastrado com sucesso!"

            connection.commit()

        except sqlite3.IntegrityError:
            return render_template(
                "pacientes.html",
                pacientes=listar_pacientes(),
                paciente_edicao=paciente_edicao,
                busca="",
                mensagem="Esse número de cadastro já está sendo utilizado."
            )

        finally:
            connection.close()

        return redirect(url_for("pacientes", mensagem=mensagem))

    busca = request.args.get("busca", "").strip()
    mensagem = request.args.get("mensagem", "")
    editar_id = request.args.get("editar", type=int)

    paciente_edicao = None

    if editar_id:
        paciente_edicao = obter_paciente(editar_id)

    return render_template(
        "pacientes.html",
        pacientes=listar_pacientes(busca),
        paciente_edicao=paciente_edicao,
        busca=busca,
        mensagem=mensagem
    )


@app.route("/visitas")
def visitas():
    return render_template("visitas.html")


if __name__ == "__main__":
    app.run(debug=True)
