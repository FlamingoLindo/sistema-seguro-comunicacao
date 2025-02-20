import os
import bcrypt

users = {}

def is_valid_email(email):
    return "@" in email and ".com" in email

def clear_screen():
    os.system('cls')

def login():
    while True:
        email = input('Digite seu e-mail: ')
        if email in users:
            password = input('Digite sua senha: ')
            if bcrypt.checkpw(password.encode('utf-8'), users[email]["password"]):
                clear_screen()
                print(f'Olá, {users[email]["name"]}!')
                break
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

def main_menu():
    while True:
        print('Já possui login?')
        print('1 - Sim')
        print('2 - Não')
        has_login = input()
        
        clear_screen()
        
        if has_login == '1':
            login()
        else:
            print('Deseja se cadastrar?')
            print('1 - Sim')
            print('2 - Não')
            register_choice = input()
            
            clear_screen()
            
            if register_choice == '1':
                register()
            else:
                print('Até mais!')
                break

if __name__ == "__main__":
    main_menu()
