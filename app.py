
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from functools import wraps
from werkzeug.security import check_password_hash
import sqlite3
import os

from database import get_connection

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


# Protege as páginas que exigem autenticação
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "id_usuario" not in session:
            return redirect(url_for("inicio"))

        return func(*args, **kwargs)

    return wrapper


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


# Login do sistema
@app.route("/", methods=["GET", "POST"])
def inicio():
    if request.method == "POST":
        login = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")

        connection = get_connection()

        try:
            usuario = connection.execute(
                """
                SELECT id_usuario, login, senha_hash
                FROM usuarios
                WHERE login = ? AND ativo = 1
                """,
                (login,)
            ).fetchone()

        finally:
            connection.close()

        if usuario and check_password_hash(usuario["senha_hash"], senha):
            session["id_usuario"] = usuario["id_usuario"]
            session["login"] = usuario["login"]

            return redirect(url_for("pacientes"))

        return render_template(
            "login.html",
            mensagem="Usuário ou senha incorretos."
        )

    return render_template("login.html")


@app.route("/pacientes", methods=["GET", "POST"])
@login_required
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


def carregar_dados_visitas():
    connection = get_connection()

    try:
        pacientes = connection.execute(
            """
            SELECT id_paciente, nome
            FROM pacientes
            WHERE ativo = 1
            ORDER BY nome
            """
        ).fetchall()

        visitas = connection.execute(
            """
            SELECT
                visitas.id_visita,
                pacientes.nome AS nome_paciente,
                visitas.data_visita,
                visitas.status,
                visitas.observacoes
            FROM visitas
            INNER JOIN pacientes
                ON pacientes.id_paciente = visitas.id_paciente
            ORDER BY visitas.data_visita DESC, visitas.id_visita DESC
            """
        ).fetchall()

        ultima_visita = connection.execute(
            """
            SELECT data_visita
            FROM visitas
            WHERE status = 'concluida'
            ORDER BY data_visita DESC, id_visita DESC
            LIMIT 1
            """
        ).fetchone()

        return pacientes, visitas, ultima_visita

    finally:
        connection.close()


@app.route("/visitas", methods=["GET", "POST"])
@login_required
def visitas():
    mensagem = request.args.get("mensagem", "")

    if request.method == "POST":
        id_paciente = request.form.get("paciente", "").strip()
        data_visita = request.form.get("data_visita", "").strip()
        status = request.form.get("status", "").strip()
        observacoes = request.form.get("observacoes", "").strip()

        if not id_paciente or not data_visita:
            mensagem = "Selecione um paciente e informe a data da visita."

        elif status not in ("agendada", "concluida", "cancelada"):
            mensagem = "Selecione um status válido."

        else:
            try:
                datetime.strptime(data_visita, "%Y-%m-%d")
            except ValueError:
                mensagem = "Informe uma data válida."

            else:
                connection = get_connection()

                try:
                    paciente = connection.execute(
                        """
                        SELECT id_paciente
                        FROM pacientes
                        WHERE id_paciente = ? AND ativo = 1
                        """,
                        (id_paciente,)
                    ).fetchone()

                    if not paciente:
                        mensagem = "Paciente não encontrado."

                    else:
                        connection.execute(
                            """
                            INSERT INTO visitas
                            (id_paciente, data_visita, status, observacoes)
                            VALUES (?, ?, ?, ?)
                            """,
                            (
                                id_paciente,
                                data_visita,
                                status,
                                observacoes or None
                            )
                        )

                        connection.commit()
                        mensagem = "Visita registrada com sucesso!"

                finally:
                    connection.close()

        return redirect(url_for("visitas", mensagem=mensagem))

    pacientes, visitas_registradas, ultima_visita = carregar_dados_visitas()

    return render_template(
        "visitas.html",
        pacientes=pacientes,
        visitas=visitas_registradas,
        ultima_visita=ultima_visita,
        mensagem=mensagem
    )


@app.route("/visitas/<int:id_visita>/status", methods=["POST"])
@login_required
def atualizar_status_visita(id_visita):
    novo_status = request.form.get("status", "").strip()

    if novo_status not in ("agendada", "concluida", "cancelada"):
        return redirect(url_for("visitas", mensagem="Status inválido."))

    connection = get_connection()

    try:
        resultado = connection.execute(
            """
            UPDATE visitas
            SET status = ?
            WHERE id_visita = ?
            """,
            (novo_status, id_visita)
        )

        connection.commit()

        if resultado.rowcount == 0:
            mensagem = "Visita não encontrada."
        else:
            mensagem = "Status da visita atualizado com sucesso!"

    finally:
        connection.close()

    return redirect(url_for("visitas", mensagem=mensagem))


# Encerramento da sessão
@app.route("/sair", methods=["POST"])
@login_required
def sair():
    session.clear()
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(debug=True)
