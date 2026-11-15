
import pytest
import database
import app as sistema

from werkzeug.security import generate_password_hash


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Cria um banco de dados temporário para os testes
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "teste.db")

    database.initialize_db()

    connection = database.get_connection()

    connection.execute(
        """
        INSERT INTO usuarios (login, senha_hash, ativo)
        VALUES (?, ?, 1)
        """,
        ("usuario_teste", generate_password_hash("senha123"))
    )

    connection.commit()
    connection.close()

    sistema.app.config["TESTING"] = True
    sistema.app.secret_key = "chave-apenas-para-testes"

    return sistema.app.test_client()


def test_login_com_credenciais_corretas(client):
    resposta = client.post(
        "/",
        data={"usuario": "usuario_teste", "senha": "senha123"}
    )

    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/pacientes")


def test_login_com_credenciais_incorretas(client):
    resposta = client.post(
        "/",
        data={"usuario": "usuario_teste", "senha": "senha_errada"}
    )

    assert resposta.status_code == 200
    assert b"Usu\xc3\xa1rio ou senha incorretos." in resposta.data


def test_acesso_a_pacientes_sem_login(client):
    resposta = client.get("/pacientes")

    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/")
