import os
import bcrypt

users = {
    "lucas@gmail.com": {
        "name": "Lucas",
        "email": "lucas@gmail.com",
        "password": bcrypt.hashpw("12345678".encode('utf-8'), bcrypt.gensalt()),
        "messages": []
    },
    "vitor@gmail.com": {
        "name": "Vitor",
        "email": "vitor@gmail.com",
        "password": bcrypt.hashpw("12345678".encode('utf-8'), bcrypt.gensalt()),
        "messages": []
    }
}

secret_key = os.urandom(16)