# Objetivos do projeto

Implementar **criptografia simétrica (AES)**, **criptografia assimétrica (RSA)**, **hashing de senhas (bcrypt)** e **autenticação com Tokens JWT (JSON Web Token)** dentro do contexto de um sistema seguro de comunicação.

---

# Tecnologias utilizadas

- `bcrypt` → Hashing seguro de senhas.
- `PyJWT` → Autenticação via Tokens JWT.
- `cryptography` → Implementação de AES e RSA

---

# Fluxo básico do sistema

- Usuário faz **cadastro** (senha armazenada com bcrypt).
    - E-mail: string, precisa ter "@dominio.com".
    - Senha: string, 8 dígitos.

- Usuário faz **login** (autenticado via JWT).
    - E-mail
    - Senha

- Usuário envia uma **mensagem criptografada com AES**.
- Apenas o destinatário correto pode **descriptografar com sua chave RSA**.
