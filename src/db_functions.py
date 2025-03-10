"""
FUNÇÕES DO BANCO DE DADOS
Este arquivo contém as funções para manipulação do banco de dados.
"""

import os
import sqlite3

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from src.load_key import secret_key

def initialize_database(db_name="sistema_segurança.db"):
    """
    Função para inicializar o banco de dados.
    Caso o banco de dados não exista, ele será criado.
    """
    db_exists = os.path.exists(db_name)
    
    con = sqlite3.connect(db_name)
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()

    if not db_exists:
        print(f"Criando banco de dados: '{db_name}'")

        # Tabel de usuários
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                token TEXT,
                attempts INTEGER DEFAULT 0,
                blocked BOOLEAN DEFAULT FALSE
            )
        ''')

        # Tabela de mensagens
        cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                message_text BLOB NOT NULL,
                message_iv BLOB NOT NULL,
                FOREIGN KEY (sender_id) REFERENCES users(id),
                FOREIGN KEY (receiver_id) REFERENCES users(id)
            )
        ''')
        con.commit()
        print("Banco criado com sucesso")

    con.close()
    
def register_user(username, email, password):
    """
    Função para registrar um usuário no banco de dados.
    """
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()

    # Insere o usuário no banco de dados
    cur.execute('''
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
    ''', (username, email, password))

    con.commit()
    con.close()
    
def get_user(email):
    """
    Função para buscar um usuário no banco de dados.
    """
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()

    # Busca o usuário no banco de dados
    cur.execute('''
        SELECT id, username, password_hash, attempts, blocked FROM users
        WHERE email = ?
    ''', (email,))
    
    user = cur.fetchone()

    # Se o usuário não existir
    if not user:
        print("Usuário não encontrado, por favor tente novamente.\n")

    con.close()
    
    return user

def update_token(token, user_id):
    """
    Função para atualizar o token de um usuário no banco de dados.
    """

    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()

    # Atualiza o token do usuário
    cur.execute("UPDATE users SET token = ? WHERE id = ?", (token, user_id))

    con.commit()
    con.close()
    
def attemp(email):
    """
    Função para atualizar a quantidade de tentativas de login de um usuário.
    """
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()

    # Atualiza a quantidade de tentativas de login
    cur.execute("UPDATE users SET attempts = attempts + 1 WHERE email = ?", (email,))
    
    # Se a quantidade de tentativas for maior ou igual a 5, bloqueia a conta
    att_amount = cur.execute("SELECT attempts FROM users WHERE email = ?", (email,)).fetchone()[0]
    if att_amount >= 5:
        cur.execute("UPDATE users SET blocked = TRUE WHERE email = ?", (email,))
        print(u'\033[4m\033[31mCONTA BLOQUEADA\033[0')
    
    con.commit()
    con.close()

def get_user_token(email):
    """
    Função para buscar o token de um usuário no banco de dados.
    """
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()

    # Busca o token do usuário
    cur.execute("SELECT token FROM users WHERE email = ?", (email,))

    token = cur.fetchone()[0]
    
    con.close()
    
    return token

"""
MESSAGES
"""

def get_all_active_users(email):
    """
    Função para buscar todos os usuários ativos no banco de dados.
    """
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()
    
    # Busca todos os usuários ativos
    query = "SELECT id, username, email FROM users WHERE blocked = 0 AND email != ?"
    cur.execute(query, (email,))
    
    users = cur.fetchall()
    con.close()
    
    return users

def show_all_active_users(email):
    """
    Função para exibir todos os usuários ativos no banco de dados.
    """
    users = get_all_active_users(email)
    
    for user in users:
        print('-' * 10)
        print(f"Nome: {user[1]} \nE-mail: {user[2]}")
        print('-' * 10)
        print()

    return users

def send_message_to_db(sender_email, receiver_email, message):
    """
    Função para enviar uma mensagem criptografada para o banco de dados.
    """
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()

    cur.execute("SELECT id FROM users WHERE email = ?", (sender_email,))
    
    sender = cur.fetchone()

    cur.execute("SELECT id FROM users WHERE email = ?", (receiver_email,))
    receiver = cur.fetchone()

    try:
        # Criptografa a mensagem
        message_bytes = message.encode('utf-8')

        # Adiciona padding na mensagem
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(message_bytes) + padder.finalize()

        # Cria um vetor de inicialização
        iv = os.urandom(16)

        # Cifra a mensagem
        cipher = Cipher(algorithms.AES(secret_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update(padded_data) + encryptor.finalize()

    except Exception as e:
        print('Erro ao criptografar a mensagem.')
        print(e)
    
    # Insere a mensagem criptografada no banco de dados
    cur.execute('''
        INSERT INTO messages (sender_id, receiver_id, message_text, message_iv)
        VALUES (?, ?, ?, ?)
    ''', (sender[0], receiver[0], encrypted_message, iv))

    con.commit()
    con.close()

def get_sent_messages(email):
    """
    Função para buscar as mensagens enviadas por um usuário.	
    """
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()

    # Busca as mensagens enviadas
    query = '''
        SELECT sender.username AS sender_name,
               receiver.username AS receiver_name,
               m.message_text AS encrypted_message,
               m.message_iv
        FROM messages m
        JOIN users sender ON m.sender_id = sender.id
        JOIN users receiver ON m.receiver_id = receiver.id
        WHERE sender.email = ?
    '''
    
    cur.execute(query, (email,))
    cryptographed_messages = cur.fetchall()

    # Se não houver mensagens enviadas
    if not cryptographed_messages:
        print("Nenhuma mensagem enviada.")
        con.close()
        return
    
    # Descriptografa as mensagens
    messages = []
    for row in cryptographed_messages:
        sender_name, receiver_name, encrypted_message, message_iv = row
        try:
            # Descriptografa a mensagem
            cipher = Cipher(algorithms.AES(secret_key), modes.CBC(message_iv))
            decryptor = cipher.decryptor()
            
            # Remove o padding da mensagem
            padded_plaintext = decryptor.update(encrypted_message) + decryptor.finalize()
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

            # Adiciona a mensagem descriptografada na lista
            messages.append((sender_name, receiver_name, encrypted_message, plaintext.decode('utf-8')))
        except Exception as e:
            print('Erro ao descriptografar a mensagem:')
            print(e)

    con.close()

    # Exibe as mensagens
    print('Mensagens enviadas:')
    for msg in messages:
        sender_name, receiver_name, enc_message, dec_message = msg
        print('-' * 10)
        print(f"De: {sender_name}\nPara: {receiver_name}")
        print(f"Mensagem criptografada (bytes): {enc_message}")
        print(f"Mensagem descriptografada: {dec_message}")
        print('-' * 10)
        print()

def get_recived_messages(email):
    """
    Função para buscar as mensagens recebidas por um usuário.
    """
    con = sqlite3.connect("sistema_segurança.db")
    cur = con.cursor()

    # Busca as mensagens recebidas
    query = '''
        SELECT sender.username AS sender_name,
               receiver.username AS receiver_name,
               m.message_text AS encrypted_message,
               m.message_iv
        FROM messages m
        JOIN users sender ON m.sender_id = sender.id
        JOIN users receiver ON m.receiver_id = receiver.id
        WHERE receiver.email = ?
    '''
    
    # Busca as mensagens criptografadas
    cur.execute(query, (email,))
    cryptographed_messages = cur.fetchall()

    # Se não houver mensagens recebidas
    if not cryptographed_messages:
        print("Nenhuma mensagem recebida.")
        con.close()
        return
    
    # Descriptografa as mensagens
    messages = []
    for row in cryptographed_messages:
        sender_name, receiver_name, encrypted_message, message_iv = row
        try:
            # Descriptografa a mensagem
            cipher = Cipher(algorithms.AES(secret_key), modes.CBC(message_iv))
            decryptor = cipher.decryptor()
            
            # Remove o padding da mensagem
            padded_plaintext = decryptor.update(encrypted_message) + decryptor.finalize()
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

            # Adiciona a mensagem descriptografada na lista
            messages.append((sender_name, receiver_name, encrypted_message, plaintext.decode('utf-8')))
        except Exception as e:
            print('Erro ao descriptografar a mensagem:')
            print(e)

    con.close()

    # Exibe as mensagens
    print('Mensagens recebidas:')
    for msg in messages:
        sender_name, receiver_name, enc_message, dec_message = msg
        print('-' * 10)
        print(f"De: {sender_name}")
        print(f"Mensagem criptografada (bytes): {enc_message}")
        print(f"Mensagem descriptografada: {dec_message}")
        print('-' * 10)
        print()