# Processo de Cadastro e Login de Usuários

O sistema de cadastro e login de usuários funciona da seguinte forma:

## Banco de Dados

O banco de dados utilizado é o `sistema_segurança.db`, que possui a tabela `users` com as seguintes colunas:

- **ID**: Identificador único do usuário.
- **Username**: Nome do usuário.
- **Email**: Endereço de e-mail do usuário (utilizado para login).
- **Password_hash**: Hash da senha do usuário.
- **Token**: Token JWT gerado para autenticação do usuário.
- **Attempts**: Número de tentativas de login falhadas.
- **Blocked**: Indica se o usuário está bloqueado.
- **Messages**: Mensagens do usuário (não implementado no código fornecido).

## Fluxo de Cadastro

O fluxo de cadastro funciona da seguinte forma:

1. O sistema solicita o nome do usuário. O nome precisa ter no mínimo 3 caracteres.
2. O sistema solicita o e-mail do usuário. O e-mail precisa conter o caractere "@" e a extensão ".com".
3. O sistema solicita a senha do usuário. A senha precisa ter no mínimo 8 caracteres.

Após as validações, a senha é criptografada utilizando o algoritmo bcrypt, e os dados do usuário (nome, e-mail e senha criptografada) são inseridos no banco de dados.

### Funções responsáveis pelo cadastro:

- **is_valid_email(email)**: Valida o formato do e-mail.
- **register()**: Função principal que executa o processo de cadastro interativo com o usuário.
- **register_user(username, email, password)**: Adiciona o usuário no banco de dados.

## Fluxo de Login

Quando o usuário deseja fazer login, o sistema segue o seguinte processo:

1. O sistema solicita o e-mail do usuário.
2. O sistema verifica se o e-mail existe no banco de dados. Caso o e-mail não exista, uma mensagem de erro é exibida.
3. Caso o e-mail seja encontrado, o sistema solicita a senha do usuário.
4. A senha fornecida é comparada com o hash armazenado no banco de dados utilizando o bcrypt. Se a senha estiver correta, um token JWT é gerado com validade de 1 dia.
5. O token gerado é armazenado no campo `Token` do usuário no banco de dados.

### Funções responsáveis pelo login:

- **login()**: Função principal que executa o processo de login interativo com o usuário.
- **get_user(email)**: Obtém as informações do usuário pelo e-mail.
- **update_token(token, user_id)**: Atualiza o token do usuário no banco de dados.
- **attemp(email)**: Incrementa o número de tentativas de login e bloqueia a conta após 5 tentativas falhas.

## Geração de Token JWT

Após a validação da senha durante o login, um token JWT é gerado com as seguintes informações:

- **email**: O e-mail do usuário.
- **exp**: A data de expiração do token, que é definida para 1 dia após a geração.

O token JWT é gerado utilizando a chave secreta `secret_key` e o algoritmo `HS256`. O token é então armazenado no banco de dados e pode ser utilizado para autenticar o usuário em futuras requisições.

## Funções Adicionais

- **attemp(email)**: Incrementa o número de tentativas de login falhadas e bloqueia a conta após 5 tentativas.
- **actions(user_email)**: Permite ao usuário realizar ações após o login, como enviar ou visualizar mensagens (funcionalidade não implementada no código fornecido).

## Resumo

O processo de cadastro e login envolve as seguintes etapas principais:

1. **Cadastro**: O usuário fornece nome, e-mail e senha, que são validados e armazenados no banco de dados.
2. **Login**: O usuário fornece e-mail e senha, e um token JWT é gerado e armazenado, permitindo acesso autenticado.
3. **Segurança**: O sistema utiliza a criptografia bcrypt para proteger as senhas e o JWT para gerenciar a autenticação de sessão.
4. **Bloqueio de conta**: O sistema bloqueia o usuário após 5 tentativas de login falhadas.

## Fluxo Completo do Sistema

1. O usuário realiza o **cadastro** fornecendo nome, e-mail e senha.
2. O sistema armazena os dados do usuário e criptografa a senha.
3. O usuário realiza o **login** com seu e-mail e senha.
4. O sistema valida a senha e gera um token JWT, que é armazenado no banco de dados.
5. O usuário pode realizar ações autenticadas, como enviar ou visualizar mensagens (funcionalidade não implementada).

O sistema permite controle de tentativas de login e bloqueio de contas em caso de múltiplas falhas.
