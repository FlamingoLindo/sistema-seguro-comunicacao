import os
import bcrypt

users = {}

def is_valid_email(email):
    return "@" in email and ".com" in email

while True:
    print('Já possui login?')
    print('1 - Sim')
    print('2 - Não')
    has_login = input()
    
    os.system('cls')
    
    if has_login == '1':
        while True:
            email = input('Digite seu e-mail: ')
            if email in users:
                password = input('Digite sua senha: ')
                if bcrypt.checkpw(password.encode('utf-8'), users[email]["password"]):
                    os.system('cls')
                    print(f'Olá, {users[email]["name"]}!')
                    break
                else:
                    os.system('cls')
                    print('Senha incorreta. Tente novamente.')
                    continue
                
            else:
                os.system('cls')
                print('E-mail não cadastrado. Tente novamente.')
                continue
        
    else:
        print('Deseja se cadastrar?')
        print('1 - Sim')
        print('2 - Não')
        register = input()
        
        os.system('cls')
        
        if register == '1':
            while True:
                name = input('Digite seu nome: ')
                if len(name) < 3:
                    os.system('cls')
                    print('O nome deve ter no mínimo 3 caracteres. Tente novamente.')
                else:
                    break
            
            while True:
                email = input('Digite seu e-mail: ')
                if is_valid_email(email):
                    break
                else:
                    os.system('cls')
                    print('O e-mail precisa ter "@" e ".com". Tente novamente.')
            
            while True:
                password = input('Digite sua senha: ')
                if len(password) < 8:
                    os.system('cls')
                    print('A senha deve ter no mínimo 8 caracteres. Tente novamente.')  
                else:
                    break
                
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            users[email] = {"name": name, "email": email, "password": hashed, "messages": []}
            
            os.system('cls')
            
            print("Usuário cadastrado com sucesso!")
            print(users)
        else:
            print('Até mais!')
            break