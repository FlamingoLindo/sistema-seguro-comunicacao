from src.utils import clear_screen
from src.user_actions import login, register
from src.db_functions import initialize_database

def logo():
    print(u'\033[31m\033[5m\033[1m')
    print(r'''
      ___                    ___                    ___     
     /  /\                  /  /\                  /  /\    
    /  /:/_                /  /:/_                /  /:/    
   /  /:/ /\              /  /:/ /\              /  /:/     
  /  /:/ /::\            /  /:/ /::\            /  /:/  ___ 
 /__/:/ /:/\:\          /__/:/ /:/\:\          /__/:/  /  /\
 \  \:\/:/~/:/          \  \:\/:/~/:/          \  \:\ /  /:/
  \  \::/ /:/            \  \::/ /:/            \  \:\  /:/ 
   \__\/ /:/              \__\/ /:/              \  \:\/:/  
     /__/:/                 /__/:/                \  \::/   
     \__\/                  \__\/                  \__\/    
    ''')
    print(u'\033[0m')
    print(u'\033[41m\033[1m\033[4mSISTEMA SEGURO DE COMUNICAÇÃO\033[0m')

def main_menu():
    while True:
        logo()
        initialize_database()
        print('Já possui login?')
        print('1 - Sim')
        print('2 - Não')
        has_login = input(u'\033[1m\033[33mInput: \033[0m')
        
        clear_screen()
        
        if has_login == '1':
            login()
        else:
            print(u'\033[33m\033[1m\033[4mDeseja se cadastrar?\033[0m')
            print('1 - Sim')
            print('2 - Não')
            register_choice = input(u'\033[1m\033[33mInput: \033[0m')
            
            clear_screen()
            
            if register_choice == '1':
                register()
            else:
                print(u'\033[33mAté mais!\033[0m')
                break
