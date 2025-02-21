import os
import datetime
import bcrypt
import jwt

from src.utils import clear_screen
from src.messages import send_message, find_messages, find_sent_messages
from src.data import users, secret_key

def is_valid_email(email):
    return "@" in email and ".com" in email

def actions(user_email):
    while True:
        clear_screen()
        action = input('Qual ação você deseja realizar:\n1 - Enviar mensagem\n2 - Ver mensagens\n3 - Sair\n')
        
        if action == '1':
            send_message(user_email)
            input("Pressione Enter para continuar...")
        elif action == '2':
            clear_screen()
            subaction = input('Ver mensagens:\n1 - Mensagens recebidas\n2 - Mensagens enviadas\nDigite sua opção: ')
            if subaction == '1':
                find_messages(user_email)
            elif subaction == '2':
                find_sent_messages(user_email)
            else:
                print('Opção inválida.')
            input("Pressione Enter para continuar...")
        elif action == '3':
            break
        else:
            print('Opção inválida.')
            input("Pressione Enter para continuar...")

def login():
    while True:
        email = input('Digite seu e-mail: ')
        if email in users:
            password = input('Digite sua senha: ')
            if bcrypt.checkpw(password.encode('utf-8'), users[email]["password"]):
                payload = {
                    "email": email,
                    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
                }
                
                token = jwt.encode(payload, secret_key, algorithm="HS256")
                users[email]["token"] = token
                
                clear_screen()
                print(f'Olá, {users[email]["name"]}!')
                actions(email)
                return email
            else:
                clear_screen()
                print('Senha incorreta. Tente novamente.')
                continue
        else:
            clear_screen()
            print('E-mail não cadastrado. Tente novamente.')
            continue

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
            
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[email] = {"name": name, "email": email, "password": hashed, "messages": []}
    
    clear_screen()
    print("Usuário cadastrado com sucesso!")
    print(users)