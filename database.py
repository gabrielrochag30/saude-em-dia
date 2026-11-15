
import sqlite3
from pathlib import Path

# Localização do banco de dados
DB_PATH = Path(__file__).resolve().parent / "saude_em_dia.db"


def get_connection():
    """Cria uma conexão com o banco de dados."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_db():
    """Cria as tabelas necessárias para o sistema."""

    connection = get_connection()

    try:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                ativo INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS pacientes (
                id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data_nascimento TEXT,
                endereco TEXT NOT NULL,
                telefone TEXT,
                numero_cadastro TEXT UNIQUE,
                ativo INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS visitas (
                id_visita INTEGER PRIMARY KEY AUTOINCREMENT,
                id_paciente INTEGER NOT NULL,
                data_visita TEXT NOT NULL,
                status TEXT NOT NULL
                    CHECK (status IN ('agendada', 'concluida', 'cancelada')),
                observacoes TEXT,

                FOREIGN KEY (id_paciente)
                    REFERENCES pacientes (id_paciente)
                    ON DELETE RESTRICT
            );

            CREATE INDEX IF NOT EXISTS idx_pacientes_nome
            ON pacientes (nome);

            CREATE INDEX IF NOT EXISTS idx_visitas_paciente_data
            ON visitas (id_paciente, data_visita);
        """)

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_db()
    print("Banco de dados e tabelas criados com sucesso!")
