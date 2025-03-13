"""
AÇÕES DO USUÁRIO
"""

import logging
import getpass
import datetime
import bcrypt
import jwt
from jwt.exceptions import ExpiredSignatureError
from cerberus import Validator

import logging_config

from src.utils import clear_screen
from src.messages import send_message
from src.db_functions import (register_user, get_user, update_token, attemp, get_sent_messages, 
                              get_recived_messages, get_user_token, delete_user)
from src.load_key import secret_key
from src.schemas import register_schema

def register():
    """
    Função para registrar um usuário no sistema.
    """

    v = Validator(register_schema)

    while True:
        username = input('Digite seu nome: ')
        if v.validate({'username': username}, update = True):
            logging.info('CADASTRO: Username valido')
            break
        else:
            clear_screen()
            logging.error('CADASTRO: username invalido: %s', v.errors['username'][0])
            print(u'\033[4m\033[31mO nome deve ter no mínimo 3 caracteres. Tente novamente.\033[0m')
            
    while True:
        email = input('Digite seu e-mail: ')
        if v.validate({'email': email}, update = True):
            logging.info('CADASTRO: Email valido')
            break
        else:
            clear_screen()
            logging.error('CADASTRO: Email invalido: %s', v.errors['email'][0])
            print(u'\033[4m\033[31mO e-mail precisa ter "@" e ".com". Tente novamente.\033[0m')
            
    while True:
        password = getpass.getpass('Digite sua senha: ')
        if v.validate({'password': password}, update = True):
            logging.info('CADASTRO: Senha valida')
            break
        else:
            clear_screen()
            logging.error('CADASTRO: Senha invalida: %s', v.errors['password'][0])
            print(u'\033[4m\033[31mA senha deve ter no mínimo 8 caracteres. Tente novamente.\033[0m')  
            
    
    # Hash da senha
    try:
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    except Exception as e:
        logging.error('CADASTRO: Erro ao fazer hashing da senha: %s', e)
        print(u'\033[1m\033[41mErro ao cadastrar usuário. Tente novamente.\033[0m')
        return
    
    # Registra o usuário no banco de dados
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
        
        # Verifica se o e-mail está cadastrado
        if user:
            user_id, username, hashed_password, attempts, role, blocked = user
            
            # Verifica se a conta está bloqueada
            if blocked:
                clear_screen()
                print(u'\033[1m\033[41mEsta conta está bloqueada. Entre em contato com o suporte.\033[0m')
                return

            password = getpass.getpass('Digite sua senha: ')
            # Verifica se a senha está correta
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                payload = {
                    "email": email,
                    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
                }
                
                # Gera o token
                token = jwt.encode(payload, secret_key, algorithm="HS256")

                # Atualiza o token no banco de dados
                update_token(token, user_id)
                logging.info(f'LOGIN: Usuario logado com sucesso: {email}')
                clear_screen()
                actions(email)

                return email
            else:
                clear_screen()
                logging.error(f'LOGIN: Senha incorreta {email}')
                print(u'\033[1m\033[41mSenha incorreta. Tente novamente.\033[0m')
                # Atualiza a quantidade de tentativas de login
                attemp(email)
                
        else:
            clear_screen()
            logging.error(f'LOGIN: Login com email nao cadastrado --> {email}')
            print(u'\033[1m\033[41mE-mail não cadastrado. Tente novamente.\033[0m')

def validate_token(user_email):
    """
    Função para validar o token do usuário.
    """

    # Verifica se o token está vazio
    token = get_user_token(user_email)
    if not token:
        clear_screen()
        logging.error(f'VALIDATE TOKEN: Token vazio --> {user_email}')
        print(u'\033[1m\033[41mToken vazio, por favor faça o login novamente.\033[0m')
        login()
        return False
    
    try:
        # Decodifica o token
        jwt.decode(token, secret_key, algorithms=["HS256"])
        logging.info(f'VALIDATE TOKEN: Token valido --> {user_email}')
    except ExpiredSignatureError:
        clear_screen()
        logging.error(f'VALIDATE TOKEN: Token expirado --> {user_email}')
        print(u'\033[1m\033[41mToken expirado, por favor faça o login novamente.\033[0m')
        login()
        return False
    except jwt.DecodeError:
        clear_screen()
        logging.error(f'VALIDATE TOKEN: Token invalido --> {user_email}')
        print(u'\033[1m\033[41mToken inválido, por favor faça o login novamente.\033[0m')
        login()
        return False

    return True

def actions(user_email):
    """
    Função para mostrar as ações disponíveis para o usuário.
    """

    user = get_user(user_email)
    user_role = user[3] if user else 'user'

    while True:
        # Valida o token
        if not validate_token(user_email):
            return

        clear_screen()
        print('Qual ação você deseja realizar:\n1 - Enviar mensagem\n2 - Ver mensagens\n3 - Alterar senha\n4 - Apagar conta\n5 - Sair')

        if user_role == 'master':
            logging.info('Usuario master acessou a plataforma')
            print('6 - Ver usuários bloqueados')

        action = input(u'\033[1m\033[33mInput: \033[0m')
        
        if action == '1':
            if not validate_token(user_email):
                return
            # Envia mensagem
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
                # Mostra mensagens recebidas
                get_recived_messages(user_email)
            elif subaction == '2':
                if not validate_token(user_email):
                    return
                clear_screen()
                # Mostra mensagens enviadas
                get_sent_messages(user_email)
            else:
                print('Opção inválida.')
                logging.error(f'Ação inválida no menu de mensagens --> {user_email}')
            input("Pressione Enter para continuar...")
        # TODO: Implementar as funções de alterar senha e apagar conta
        elif action == '3':
            print('alterar senha')
        elif action == '4':
            clear_screen()
            print('Você deseja apagar sua conta?')
            print('1 - Sim\n2 - Não')
            action = input(u'\033[1m\033[33mInput: \033[0m')
            if action == '1':
                delete_user(user_email)
                print('Conta apagada com sucesso.')
                input("Pressione Enter para continuar...")
                break
            else:
                input("Pressione Enter para continuar...")
            
        elif action == '5':
            break
        else:
            print('Opção inválida.')
            logging.error(f'Ação inválida no menu principal --> {user_email}')
            input("Pressione Enter para continuar...")
