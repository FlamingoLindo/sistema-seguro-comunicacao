import os
import time
import sqlite3
import datetime
import bcrypt
import jwt
from jwt.exceptions import ExpiredSignatureError

from src.utils import clear_screen

secret_key = os.urandom(16)

def is_valid_email(email):
    return "@" in email and ".com" in email

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

def generate_password_hash(password, method='bcrypt'):
    if method == 'bcrypt':
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def add_user(username, password):
    password_hash = generate_password_hash(password, method='bcrypt') 
    cursor.execute(''' 
        INSERT INTO usuario (username, password_hash)
        VALUES (?, ?)
    ''', (username, password_hash))
    conn.commit()


def is_valid_email(email):
    return '@' in email and '.com' in email

def register():
    while True:
        name = input('Digite seu nome: ')
        if len(name) < 3:
            clear_screen()
            print('O nome deve ter no mínimo 3 caracteres. Tente novamente.')
        else:
            break
    
    while True:
        email = input('Digite seu e-mail: ')
        if is_valid_email(email):
            break
        else:
            clear_screen()
            print('O e-mail precisa ter "@" e ".com". Tente novamente.')
    
    while True:
        password = input('Digite sua senha: ')
        if len(password) < 8:
            clear_screen()
            print('A senha deve ter no mínimo 8 caracteres. Tente novamente.')  
        else:
            break
            
    add_user(email, password)  
    
    clear_screen()
    print("Usuário cadastrado com sucesso!")

def generate_password_hash(password, method='bcrypt'):
    if method == 'bcrypt':
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def add_user(username, password):
    password_hash = generate_password_hash(password, method='bcrypt')  
    cursor.execute(''' 
        INSERT INTO usuario (username, password_hash)
        VALUES (?, ?)
    ''', (username, password_hash))
    conn.commit()

def login():
    while True:
        email = input('Digite seu e-mail: ')
        cursor.execute("SELECT * FROM usuario WHERE username = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            password = input('Digite sua senha: ')
            stored_password_hash = user[2].encode('utf-8')
            
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
                payload = {
                    "email": email,
                    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
                }
                
                token = jwt.encode(payload, secret_key, algorithm="HS256")
                
                cursor.execute('''UPDATE usuario SET token = ? WHERE username = ?''', (token, email))
                conn.commit()
                
                clear_screen()
                print(f'Olá, {email}!')
                
                # Apenas provisorio
                time.sleep(1000)
                
            else:
                clear_screen()
                print('Senha incorreta. Tente novamente.')
                continue
        else:
            clear_screen()
            print('E-mail não cadastrado. Tente novamente.')
            continue


def user_has_token(user_email):
    cursor.execute("SELECT token FROM usuario WHERE username = ?", (user_email,))
    token_data = cursor.fetchone()
    
    if token_data and token_data[0]:
        try:
            jwt.decode(token_data[0], secret_key, algorithms=["HS256"], options={"verify_exp": True})
            return True
        except jwt.ExpiredSignatureError:
            print('Token expirado. Faça login novamente.')
            return False
    else:
        print('Acesso negado. Faça login para continuar.')
        return False


