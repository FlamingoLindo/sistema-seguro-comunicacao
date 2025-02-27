import os
import datetime
import bcrypt
import jwt
from jwt.exceptions import ExpiredSignatureError

from src.utils import clear_screen
<<<<<<< HEAD
# from src.messages import send_message, find_messages, find_sent_messages
from src.db_functions import register_user, get_user, update_token, attemp
from src.data import secret_key
=======
from src.messages import send_message, find_recived_messages, find_sent_messages
from src.data import users, secret_key
>>>>>>> 6971d2a264c5307f61802a5df475cf6860ae390a

def is_valid_email(email):
    return "@" in email and ".com" in email

<<<<<<< HEAD
=======
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

>>>>>>> 6971d2a264c5307f61802a5df475cf6860ae390a
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
<<<<<<< HEAD

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
=======
    print(users)

def user_has_token(user_email):
    if "token" in users[user_email] and users[user_email]["token"]:
        try:
            jwt.decode(users[user_email]["token"], secret_key, algorithms=["HS256"], options={"verify_exp": True})
            return True
        except ExpiredSignatureError:
            print('Token expirado. Faça login novamente.')
            return False
    else:
        print('Acesso negado. Faça login para continuar.')
        return False
>>>>>>> 6971d2a264c5307f61802a5df475cf6860ae390a

def actions(user_email):
    while True:
        clear_screen()
<<<<<<< HEAD
        action = input('Qual ação você deseja realizar:\n1 - Enviar mensagem\n2 - Ver mensagens\n3 - Sair\n')
        
        if action == '1':
            #send_message(user_email)
=======
        user_has_token(user_email)
        action = input('Qual ação você deseja realizar:\n1 - Enviar mensagem\n2 - Ver mensagens\n3 - Sair\n')
        
        if action == '1':
            send_message(user_email)
>>>>>>> 6971d2a264c5307f61802a5df475cf6860ae390a
            input("Pressione Enter para continuar...")
        elif action == '2':
            clear_screen()
            subaction = input('Ver mensagens:\n1 - Mensagens recebidas\n2 - Mensagens enviadas\nDigite sua opção: ')
<<<<<<< HEAD
            # if subaction == '1':
            #     find_messages(user_email)
            # elif subaction == '2':
            #     find_sent_messages(user_email)
            # else:
            #     print('Opção inválida.')
=======
            if subaction == '1':
                find_recived_messages(user_email)
            elif subaction == '2':
                find_sent_messages(user_email)
            else:
                print('Opção inválida.')
>>>>>>> 6971d2a264c5307f61802a5df475cf6860ae390a
            input("Pressione Enter para continuar...")
        elif action == '3':
            break
        else:
            print('Opção inválida.')
<<<<<<< HEAD
            input("Pressione Enter para continuar...")
=======
            input("Pressione Enter para continuar...")
>>>>>>> 6971d2a264c5307f61802a5df475cf6860ae390a
