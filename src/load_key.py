"""
CARREGAR A CHAVE SECRETA DO ARQUIVO .env
"""

import os
import binascii
from dotenv import load_dotenv

load_dotenv()

hex_key = os.getenv("SECRET_KEY")
if not hex_key:
    raise ValueError("NÃO EXISTE UMA CHAVE SECRETA DEFINIDA")

secret_key = binascii.unhexlify(hex_key)
