import os
import binascii
from dotenv import load_dotenv

load_dotenv()

hex_key = os.getenv("SECRET_KEY")
if not hex_key:
    raise ValueError("SECRET_KEY environment variable is not set!")

secret_key = binascii.unhexlify(hex_key)
