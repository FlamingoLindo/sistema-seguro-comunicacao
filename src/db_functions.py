"""
FUNCOES DO BANCO DE DADOS
Este arquivo contem as funcoes para manipulacao do banco de dados.
"""

import logging
import os
import sqlite3

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

import logging_config

from src.load_key import secret_key


def initialize_database(db_name="sistema_seguranca.db"):
    """
    Funcao para inicializar o banco de dados.
    Caso o banco de dados nao exista, ele sera criado.
    """
    try:
        db_exists = os.path.exists(db_name)
        con = sqlite3.connect(db_name)
        con.execute("PRAGMA foreign_keys = ON")
        cur = con.cursor()

        if not db_exists:
            logging.info("Inicializando o banco de dados: '%s'", db_name)
            print(f"Criando banco de dados: '{db_name}'")

            # Tabela de usuarios
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    cpf TEXT unique,
                    phone TEXT unique,
                    cep TEXT,
                    street TEXT,
                    number TEXT,
                    complement TEXT,
                    city TEXT,
                    state TEXT,
                    role TEXT DEFAULT 'user',
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
            logging.info("Banco de dados criado com sucesso!")
        else:
            logging.info("Banco de dados '%s' ja existe.", db_name)
    except Exception as e:
        logging.error("Erro ao inicializar o banco de dados: %s", e)
    finally:
        try:
            con.close()
        except Exception:
            pass


def register_user(username, email, password, cpf, phone, cep, street, number, complement, city, state):
    """
    Funcao para registrar um usuario no banco de dados.
    """
    con = None
    try:
        con = sqlite3.connect("sistema_seguranca.db")
        cur = con.cursor()
        cur.execute('''
            INSERT INTO users (username, email, password_hash, cpf, phone, cep, street, number, complement, city, state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, password, cpf, phone, cep, street, number, complement, city, state))
        con.commit()
        logging.info("Usuario '%s' registrado com sucesso.", username)
    except sqlite3.IntegrityError as e:
        logging.error("Integrity error ao registrar o usuario '%s': %s", username, e)
    except sqlite3.Error as e:
        logging.error("Database error ao registrar o usuario '%s': %s", username, e)
        raise
    finally:
        if con:
            con.close()


def get_user(email):
    """
    Funcao para buscar um usuario no banco de dados.
    """
    con = None
    try:
        con = sqlite3.connect("sistema_seguranca.db")
        cur = con.cursor()
        cur.execute('''
            SELECT id, username, password_hash, role, attempts, blocked FROM users
            WHERE email = ?
        ''', (email,))
        user = cur.fetchone()
        if not user:
            logging.info("Usuario com email '%s' nao encontrado.", email)
            print("Usuario nao encontrado, por favor tente novamente.\n")
        else:
            logging.info("Usuario com email '%s' encontrado.", email)
        return user
    except sqlite3.Error as e:
        logging.error("Erro ao buscar usuario com email '%s': %s", email, e)
        return None
    finally:
        if con:
            con.close()


def update_token(token, user_id):
    """
    Funcao para atualizar o token de um usuario no banco de dados.
    """
    con = None
    try:
        con = sqlite3.connect("sistema_seguranca.db")
        cur = con.cursor()
        cur.execute("UPDATE users SET token = ? WHERE id = ?", (token, user_id))
        con.commit()
        logging.info("Token atualizado para o usuario ID: %s", user_id)
    except sqlite3.Error as e:
        logging.error("Erro ao atualizar token para o usuario ID '%s': %s", user_id, e)
    finally:
        if con:
            con.close()


def attemp(email):
    """
    Funcao para atualizar a quantidade de tentativas de login de um usuario.
    """
    con = None
    try:
        con = sqlite3.connect("sistema_seguranca.db")
        cur = con.cursor()
        cur.execute("UPDATE users SET attempts = attempts + 1 WHERE email = ?", (email,))
        att_amount = cur.execute("SELECT attempts FROM users WHERE email = ?", (email,)).fetchone()[0]
        logging.info("Tentativas atualizadas para o usuario '%s': %s", email, att_amount)
        if att_amount >= 5:
            cur.execute("UPDATE users SET blocked = TRUE WHERE email = ?", (email,))
            print(u'\033[4m\033[31mCONTA BLOQUEADA\033[0m')
            logging.warning("Conta do usuario '%s' bloqueada por tentativas excessivas.", email)
        con.commit()
    except sqlite3.Error as e:
        logging.error("Erro ao atualizar tentativas para o usuario '%s': %s", email, e)
    finally:
        if con:
            con.close()


def get_user_token(email):
    """
    Funcao para buscar o token de um usuario no banco de dados.
    """
    con = None
    try:
        con = sqlite3.connect("sistema_seguranca.db")
        cur = con.cursor()
        cur.execute("SELECT token FROM users WHERE email = ?", (email,))
        result = cur.fetchone()
        if result:
            token = result[0]
            logging.info("Token recuperado para o usuario '%s'.", email)
        else:
            token = None
            logging.info("Nenhum token encontrado para o usuario '%s'.", email)
        return token
    except sqlite3.Error as e:
        logging.error("Erro ao buscar token para o usuario '%s': %s", email, e)
        return None
    finally:
        if con:
            con.close()

def delete_user(email):
    """
    Funcao para deletar um usuario do banco de dados.
    """
    con = None
    try:
        con = sqlite3.connect("sistema_seguranca.db")
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE email = ?", (email,))
        con.commit()
        if cur.rowcount > 0:
            logging.info("Usuario '%s' deletado com sucesso.", email)
            return True
        else:
            logging.info("Nenhum usuario encontrado com o email '%s'.", email)
            return False
    except sqlite3.Error as e:
        logging.error("Erro ao deletar usuario '%s': %s", email, e)
        return False
    finally:
        if con:
            con.close()


"""
MESSAGES
"""

def get_all_active_users(email):
    """
    Funcao para buscar todos os usuarios ativos no banco de dados.
    """
    con = None
    try:
        con = sqlite3.connect("sistema_seguranca.db")
        cur = con.cursor()
        query = "SELECT id, username, email FROM users WHERE blocked = 0 AND email != ?"
        cur.execute(query, (email,))
        users = cur.fetchall()
        logging.info("Usuarios ativos recuperados (excluindo '%s').", email)
        return users
    except sqlite3.Error as e:
        logging.error("Erro ao recuperar usuarios ativos (excluindo '%s'): %s", email, e)
        return []
    finally:
        if con:
            con.close()


def show_all_active_users(email):
    """
    Funcao para exibir todos os usuarios ativos no banco de dados.
    """
    try:
        users = get_all_active_users(email)
        for user in users:
            print('-' * 10)
            print(f"Nome: {user[1]} \nEmail: {user[2]}")
            print('-' * 10)
            print()
        logging.info("Exibidos todos os usuarios ativos (excluindo '%s').", email)
        return users
    except Exception as e:
        logging.error("Erro ao exibir usuarios ativos: %s", e)
        return []


def send_message_to_db(sender_email, receiver_email, message):
    """
    Funcao para enviar uma mensagem criptografada para o banco de dados.
    """
    con = None
    try:
        con = sqlite3.connect("sistema_seguranca.db")
        cur = con.cursor()

        # Recupera os IDs do remetente e destinatario
        cur.execute("SELECT id FROM users WHERE email = ?", (sender_email,))
        sender = cur.fetchone()
        cur.execute("SELECT id FROM users WHERE email = ?", (receiver_email,))
        receiver = cur.fetchone()

        if not sender or not receiver:
            logging.error("Remetente ou destinatario nao encontrados (sender: '%s', receiver: '%s')", sender_email, receiver_email)
            print("Erro: Remetente ou destinatario nao encontrado.")
            return

        try:
            # Criptografa a mensagem
            message_bytes = message.encode('utf-8')
            padder = padding.PKCS7(algorithms.AES.block_size).padder()
            padded_data = padder.update(message_bytes) + padder.finalize()
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(secret_key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
            logging.info("Mensagem criptografada com sucesso.")
        except Exception as e:
            logging.error("Erro ao criptografar a mensagem: %s", e)
            print("Erro ao criptografar a mensagem.")
            return

        cur.execute('''
            INSERT INTO messages (sender_id, receiver_id, message_text, message_iv)
            VALUES (?, ?, ?, ?)
        ''', (sender[0], receiver[0], encrypted_message, iv))
        con.commit()
        logging.info("Mensagem enviada de '%s' para '%s'.", sender_email, receiver_email)
    except sqlite3.Error as e:
        logging.error("Erro ao enviar mensagem de '%s' para '%s': %s", sender_email, receiver_email, e)
    finally:
        if con:
            con.close()


def get_sent_messages(email):
    """
    Funcao para buscar as mensagens enviadas por um usuario.
    """
    con = None
    try:
        con = sqlite3.connect("sistema_seguranca.db")
        cur = con.cursor()
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

        if not cryptographed_messages:
            logging.info("Nenhuma mensagem enviada encontrada para o usuario '%s'.", email)
            print("Nenhuma mensagem enviada.")
            return

        messages = []
        for row in cryptographed_messages:
            sender_name, receiver_name, encrypted_message, message_iv = row
            try:
                cipher = Cipher(algorithms.AES(secret_key), modes.CBC(message_iv))
                decryptor = cipher.decryptor()
                padded_plaintext = decryptor.update(encrypted_message) + decryptor.finalize()
                unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
                messages.append((sender_name, receiver_name, encrypted_message, plaintext.decode('utf-8')))
            except Exception as e:
                logging.error("Erro ao descriptografar mensagem enviada: %s", e)
                print("Erro ao descriptografar a mensagem.")
        logging.info("Mensagens enviadas recuperadas para o usuario '%s'.", email)
    except sqlite3.Error as e:
        logging.error("Erro ao recuperar mensagens enviadas para o usuario '%s': %s", email, e)
    finally:
        if con:
            con.close()

    # Exibe as mensagens
    print("Mensagens enviadas:")
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
    Funcao para buscar as mensagens recebidas por um usuario.
    """
    con = None
    try:
        con = sqlite3.connect("sistema_seguranca.db")
        cur = con.cursor()
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
        cur.execute(query, (email,))
        cryptographed_messages = cur.fetchall()

        if not cryptographed_messages:
            logging.info("Nenhuma mensagem recebida encontrada para o usuario '%s'.", email)
            print("Nenhuma mensagem recebida.")
            return

        messages = []
        for row in cryptographed_messages:
            sender_name, receiver_name, encrypted_message, message_iv = row
            try:
                cipher = Cipher(algorithms.AES(secret_key), modes.CBC(message_iv))
                decryptor = cipher.decryptor()
                padded_plaintext = decryptor.update(encrypted_message) + decryptor.finalize()
                unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
                messages.append((sender_name, receiver_name, encrypted_message, plaintext.decode('utf-8')))
            except Exception as e:
                logging.error("Erro ao descriptografar mensagem recebida: %s", e)
                print("Erro ao descriptografar a mensagem.")
        logging.info("Mensagens recebidas recuperadas para o usuario '%s'.", email)
    except sqlite3.Error as e:
        logging.error("Erro ao recuperar mensagens recebidas para o usuario '%s': %s", email, e)
    finally:
        if con:
            con.close()

    # Exibe as mensagens
    print("Mensagens recebidas:")
    for msg in messages:
        sender_name, receiver_name, enc_message, dec_message = msg
        print('-' * 10)
        print(f"De: {sender_name}")
        print(f"Mensagem criptografada (bytes): {enc_message}")
        print(f"Mensagem descriptografada: {dec_message}")
        print('-' * 10)
        print()