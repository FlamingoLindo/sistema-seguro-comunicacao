import sqlite3
import os

def initialize_database(db_name="sistema_segurança.db"):
    db_exists = os.path.exists(db_name)
    
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    if not db_exists:
        print(f"Criando banco de dados: '{db_name}'")

        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                token TEXT,
                attempts INTEGER DEFAULT 0,
                blocked BOOLEAN DEFAULT FALSE,
                messages TEXT
            )
        ''')
        con.commit()
        print("Banco criado com sucesso")

    con.close()
    
def register_user(username, email, password):
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()

    cur.execute('''
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    ''', (username, email, password))

    con.commit()
    con.close()
    
def get_user(email):
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()

    cur.execute('''
        SELECT id, username, password_hash, attempts, blocked FROM users
        WHERE email = ?
    ''', (email,))
    
    user = cur.fetchone()
    con.close()
    
    return user

def update_token(token, user_id):
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET token = ? WHERE id = ?", (token, user_id))
    con.commit()
    con.close()
    
def attemp(email):
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET attempts = attempts + 1 WHERE email = ?", (email,))
    
    att_amount = cur.execute("SELECT attempts FROM users WHERE email = ?", (email,)).fetchone()[0]
    if att_amount >= 5:
        cur.execute("UPDATE users SET blocked = TRUE WHERE email = ?", (email,))
        print('CONTA BLOQUEADA')
    
    con.commit()
    con.close()