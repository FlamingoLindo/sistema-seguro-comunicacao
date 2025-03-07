"""
AÇÕES DO USUÁRIO
"""

import getpass
import datetime
import bcrypt
import jwt
from jwt.exceptions import ExpiredSignatureError

from src.utils import clear_screen
from src.messages import send_message
from src.db_functions import (register_user, get_user, update_token, attemp, get_sent_messages, 
                              get_recived_messages, get_user_token)
from src.load_key import secret_key

def is_valid_email(email):
    """
    Função para verificar se o e-mail é válido.
    """

    return "@" in email and ".com" in email

def register():
    """
    Função para registrar um usuário no sistema.
    """

    while True:
        username = input('Digite seu nome: ')
        if len(username) < 3:
            clear_screen()
            print(u'\033[4m\033[31mO nome deve ter no mínimo 3 caracteres. Tente novamente.\033[0m')
        else:
            break
    
    while True:
        email = input('Digite seu e-mail: ')
        if is_valid_email(email):
            break
        else:
            clear_screen()
            print(u'\033[4m\033[31mO e-mail precisa ter "@" e ".com". Tente novamente.\033[0m')
    
    while True:
        password = getpass.getpass('Digite sua senha: ')
        if len(password) < 8:
            clear_screen()
            print(u'\033[4m\033[31mA senha deve ter no mínimo 8 caracteres. Tente novamente.\033[0m')  
        else:
            break
            
    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    register_user(username, email, password)
    
    clear_screen()
    print(u"\033[1m\033[32mUsuário cadastrado com sucesso!\033[0m")

def login():
    """
    Função para fazer login no sistema.
    """

    while True:
        email = input('Digite seu e-mail: ')
        user = get_user(email)
        
        if user:
            user_id, username, hashed_password, attempts, blocked = user

            if blocked:
                clear_screen()
                print(u'\033[1m\033[41mEsta conta está bloqueada. Entre em contato com o suporte.\033[0m')
                return

            password = getpass.getpass('Digite sua senha: ')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                payload = {
                    "email": email,
                    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
                }
                
                token = jwt.encode(payload, secret_key, algorithm="HS256")

                update_token(token, user_id)

                clear_screen()
                actions(email)
                return email
            else:
                clear_screen()
                print(u'\033[1m\033[41mSenha incorreta. Tente novamente.\033[0m')
                attemp(email)
                
        else:
            clear_screen()
            print(u'\033[1m\033[41mE-mail não cadastrado. Tente novamente.\033[0m')

def validate_token(user_email):
    """
    Função para validar o token do usuário.
    """

    token = get_user_token(user_email)
    if not token:
        clear_screen()
        print(u'\033[1m\033[41mToken vazio, por favor faça o login novamente.\033[0m')
        login()
        return False
    
    try:
        jwt.decode(token, secret_key, algorithms=["HS256"])
    except ExpiredSignatureError:
        clear_screen()
        print(u'\033[1m\033[41mToken expirado, por favor faça o login novamente.\033[0m')
        login()
        return False
    except jwt.DecodeError:
        clear_screen()
        print(u'\033[1m\033[41mToken inválido, por favor faça o login novamente.\033[0m')
        login()
        return False

    return True

def actions(user_email):
    """
    Função para mostrar as ações disponíveis para o usuário.
    """

    while True:
        if not validate_token(user_email):
            return

        clear_screen()
        print('Qual ação você deseja realizar:\n1 - Enviar mensagem\n2 - Ver mensagens\n3 - Sair')
        action = input(u'\033[1m\033[33mInput: \033[0m')
        
        if action == '1':
            if not validate_token(user_email):
                return
            send_message(user_email)
            input("Pressione Enter para continuar...")
        elif action == '2':
            if not validate_token(user_email):
                return

            clear_screen()
            print('Ver mensagens:\n1 - Mensagens recebidas\n2 - Mensagens enviadas')
            subaction = input(u'\033[1m\033[33mInput: \033[0m')

            if subaction == '1':
                if not validate_token(user_email):
                    return
                clear_screen()
                get_recived_messages(user_email)
            elif subaction == '2':
                if not validate_token(user_email):
                    return
                clear_screen()
                get_sent_messages(user_email)
            else:
                print('Opção inválida.')
            input("Pressione Enter para continuar...")
        elif action == '3':
            break
        else:
            print('Opção inválida.')
            input("Pressione Enter para continuar...")
