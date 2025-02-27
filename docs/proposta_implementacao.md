# Como cada tecnologia será usada no sistema

## Bcrypt

Criação de hash senhas

_Versão: 4.2.1_


## PyJWT

Criação e leitura de tokens JWT

_Versão: 2.10.1_

## Cryptography

Criptografia do tipo AES e RSA

_Versão: 44.0.1_

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
