import jwt
import datetime

email = 'vitor@gmail.com'
password = '12345678'

secret_key = "secret"

payload = {
    "email": email,
    "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
}

token = jwt.encode(payload, secret_key, algorithm="HS256")

print(token)

decoded = jwt.decode(token, secret_key, algorithms=["HS256"])

print(decoded)
