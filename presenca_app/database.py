# database.py
import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('presenca.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Criar tabelas se não existirem
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS membros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            funcao TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data TEXT NOT NULL,
            tipo TEXT NOT NULL -- 'ensaio' ou 'culto'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presencas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            membro_id INTEGER NOT NULL,
            evento_id INTEGER NOT NULL,
            presente BOOLEAN NOT NULL,
            FOREIGN KEY (membro_id) REFERENCES membros (id),
            FOREIGN KEY (evento_id) REFERENCES eventos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_membros():
    conn = get_db_connection()
    membros = conn.execute('SELECT * FROM membros').fetchall()
    conn.close()
    return [dict(membro) for membro in membros]

def get_eventos():
    conn = get_db_connection()
    eventos = conn.execute('SELECT * FROM eventos ORDER BY data DESC').fetchall()
    conn.close()
    return [dict(evento) for evento in eventos]

def get_presencas():
    conn = get_db_connection()
    presencas = conn.execute('SELECT * FROM presencas').fetchall()
    conn.close()
    return [dict(presenca) for presenca in presencas]

def registrar_presenca(membro_id, evento_id, presente):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO presencas (membro_id, evento_id, presente) VALUES (?, ?, ?)',
        (membro_id, evento_id, presente)
    )
    conn.commit()
    conn.close()

# Adicionado estas novas funções ao database
def adicionar_membro(nome, funcao):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO membros (nome, funcao) VALUES (?, ?)',
        (nome, funcao)
    )
    conn.commit()
    conn.close()

def adicionar_evento(nome, data, tipo):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO eventos (nome, data, tipo) VALUES (?, ?, ?)',
        (nome, data, tipo)
    )
    conn.commit()
    conn.close()

# Inicializar o banco de dados
init_db()