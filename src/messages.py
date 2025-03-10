"""ENVIO DE MENSAGEM"""

from src.utils import clear_screen
from src.db_functions import show_all_active_users, get_user, send_message_to_db

def send_message(email):
    """
    Função para enviar uma mensagem criptografada para outro usuário.
    """

    clear_screen()
    print('Escolha um usuário para enviar a mensagem:\n')
    
    # Mostra todos os usuários ativos
    active_users = show_all_active_users(email)
    
    # Se não houver usuários ativos
    if not active_users:
        print('Não há usuários disponíveis para enviar mensagens.')
        return

    while True:
        recipient_email = input('Digite o e-mail do usuário: ')

        # Verifica se o e-mail é válido
        recipient = get_user(recipient_email)

        if recipient is None:
            print("Usuário não encontrado, tente novamente.\n")
            continue
        
        message = input('Digite a mensagem: ')

        # Envia a mensagem para o banco de dados
        send_message_to_db(email, recipient_email, message)

        print(f"Mensagem criptografada e enviada para {recipient_email}")
        break