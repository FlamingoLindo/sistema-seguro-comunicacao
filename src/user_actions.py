import os
import datetime
import bcrypt
import jwt

from src.utils import clear_screen
# from src.messages import send_message, find_messages, find_sent_messages
from src.db_functions import register_user, get_user, update_token, attemp
from src.data import secret_key

def is_valid_email(email):
    return "@" in email and ".com" in email

def register():
    while True:
        username = input('Digite seu nome: ')
        if len(username) < 3:
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
            
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    register_user(username, email, password)
    
    clear_screen()
    print("Usuário cadastrado com sucesso!")

def login():
    while True:
        email = input('Digite seu e-mail: ')
        user = get_user(email)
        
        if user:
            user_id, username, hashed_password, attempts, blocked = user

            if blocked:
                clear_screen()
                print('Esta conta está bloqueada. Entre em contato com o suporte.')
                return

            password = input('Digite sua senha: ')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                payload = {
                    "email": email,
                    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
                }
                
                token = jwt.encode(payload, secret_key, algorithm="HS256")

                update_token(token, user_id)

                clear_screen()
                print(f'Olá, {username}!')
                actions(email)
                return email
            else:
                clear_screen()
                attemp(email)
                print('Senha incorreta. Tente novamente.')
        else:
            clear_screen()
            print('E-mail não cadastrado. Tente novamente.')

def actions(user_email):
    while True:
        clear_screen()
        action = input('Qual ação você deseja realizar:\n1 - Enviar mensagem\n2 - Ver mensagens\n3 - Sair\n')
        
        if action == '1':
            #send_message(user_email)
            input("Pressione Enter para continuar...")
        elif action == '2':
            clear_screen()
            subaction = input('Ver mensagens:\n1 - Mensagens recebidas\n2 - Mensagens enviadas\nDigite sua opção: ')
            # if subaction == '1':
            #     find_messages(user_email)
            # elif subaction == '2':
            #     find_sent_messages(user_email)
            # else:
            #     print('Opção inválida.')
            input("Pressione Enter para continuar...")
        elif action == '3':
            break
        else:
            print('Opção inválida.')
            input("Pressione Enter para continuar...")