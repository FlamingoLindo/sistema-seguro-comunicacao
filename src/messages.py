import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

from src.data import users
from src.utils import clear_screen

key = os.urandom(32)

def show_all_users():
    for user in users:
        print(user)

def send_message(user_email):
    print('Escolha um usuário para enviar a mensagem:')
    show_all_users()
    recipient_user = input('Digite o e-mail do usuário: ')
    message = input('Digite a mensagem: ')
    
    try:
        message_bytes = message.encode('utf-8')
        padder = padding.PKCS7(algorithms.AES.block_size).padder()  
        padded_data = padder.update(message_bytes) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update(padded_data) + encryptor.finalize()

        if recipient_user in users:
            encrypted_payload = {
                "iv": iv,
                "message": encrypted_message,
                "sender": user_email
            }
            users[recipient_user]["messages"].append(encrypted_payload)

            if "sent_messages" not in users[user_email]:
                users[user_email]["sent_messages"] = []
            users[user_email]["sent_messages"].append({
                "to": recipient_user,
                "message": encrypted_payload
            })
            print('Mensagem criptografada e enviada com sucesso!')

        else:
            print('Usuário não encontrado.')
    
    except Exception as e:
        print('Erro ao criptografar a mensagem.')
        print(e)

    

def find_recived_messages(user_email):
    clear_screen()
    print('Mensagens recebidas:')
    
    try:
        messages = users[user_email]["messages"]
        if not messages:
            print("Nenhuma mensagem recebida.")
        else:
            for payload in messages:
                iv = payload["iv"]
                encrypted_message = payload["message"]
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
                decryptor = cipher.decryptor()
                padded_plaintext = decryptor.update(encrypted_message) + decryptor.finalize()
                
                unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
                
                print(f"De: {payload['sender']}\nMensagem: {plaintext.decode('utf-8')}\n")
                
    except Exception as e:
        print("Erro ao descriptografar a mensagem.")
        print(e)

def find_sent_messages(user_email):
    clear_screen()
    print('Mensagens enviadas:')
    
    try:
        sent_messages = users[user_email].get("sent_messages", [])
        if not sent_messages:
            print("Nenhuma mensagem enviada.")
        else:
            for sent in sent_messages:
                iv = sent['message']['iv']
                encrypted_message = sent['message']['message']
                cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
                decryptor = cipher.decryptor()
                padded_plaintext = decryptor.update(encrypted_message) + decryptor.finalize()
                
                unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
                plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
                
                print(f"Para: {sent['to']}\nMensagem: {plaintext.decode('utf-8')}\n")
                
    except Exception as e:
        print('Erro ao descriptografar a mensagem.')
        print(e)