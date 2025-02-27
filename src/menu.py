from src.utils import clear_screen
from src.user_actions import login, register
from src.db_functions import initialize_database

def main_menu():
    while True:
        initialize_database()
        clear_screen()
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
