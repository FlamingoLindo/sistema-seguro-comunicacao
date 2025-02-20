# Como cada tecnologia será usada no sistema

## Bcrypt

Será utilizado para criação de hash senhas

Versão: 4.2.1


## PyJWT

Criação e leitura de tokens JWT

Versão: 2.10.1

## Cryptography

Criptografia dotipo AES e RSA

Versões: cffi-1.17.1, cryptography-44.0.1, pycparser-2.22 

---

# Principais etapas de implementação

- Cadastro de usuário → Hash de senha com bcrypt.
- Login → Geração e verificação de Token JWT.
- Criptografia de mensagens → Uso de AES (CBC).
- Proteção da chave AES → Uso de RSA para criptografar a chave antes de armazená-la.

---

# Armazenamento seguro de dados

1. Todas as senhas dos usuários deveram ser obrigatoriamente passadas pelo processo de _hash_.

2. Todas as mensagens deveram ser criptografadas usando o padrão AES (CBC)

3. Todas as chaves AES deveram ser criptografadas antes de serem armazenadas utilizando RSA.
