from src.data import users
from src.utils import clear_screen

def show_all_users():
    for user in users:
        print(user)
    return True

def send_message(user_email):
    print('Escolha um usuário para enviar a mensagem:')
    show_all_users()
    recipient_user = input('Digite o e-mail do usuário: ')
    message = input('Digite a mensagem: ')
    
    if recipient_user in users:
        users[recipient_user]["messages"].append(message)

        if "sent_messages" not in users[user_email]:
            users[user_email]["sent_messages"] = []
        users[user_email]["sent_messages"].append({
            "to": recipient_user,
            "message": message
        })
        print('Mensagem enviada com sucesso!')
        return True
    else:
        print('Usuário não encontrado.')
        return False

def find_messages(user_email):
    clear_screen()
    print('Mensagens recebidas:')
    for message in users[user_email]["messages"]:
        print(message)

def find_sent_messages(user_email):
    clear_screen()
    print('Mensagens enviadas:')
    sent_messages = users[user_email].get("sent_messages", [])
    if not sent_messages:
        print("Nenhuma mensagem enviada.")
    else:
        for sent in sent_messages:
            print(f"Para: {sent['to']}\nMensagem: {sent['message']}\n")