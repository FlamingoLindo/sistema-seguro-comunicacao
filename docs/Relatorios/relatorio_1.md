# Processo de Cadastro e Login de Usuários

O sistema de cadastro e login de usuários funciona da seguinte forma:

## Banco de Dados

Primeiramente, é criado o banco de dados `users.db` com uma tabela chamada `usuario`, que possui as seguintes colunas:

- `ID`: Identificador único do usuário.
- `Username`: Endereço de e-mail do usuário (será usado como nome de usuário).
- `Password_hash`: Hash da senha do usuário.
- `Token`: Token JWT gerado para autenticação do usuário.
- `Blocked`: Indica se o usuário está bloqueado (campo não implementado no código fornecido, mas pode ser adicionado futuramente).
- `Attempts`: Número de tentativas de login falhadas (campo não implementado no código fornecido, mas pode ser adicionado futuramente).

## Fluxo de Cadastro

Quando o usuário deseja se cadastrar, o sistema realiza o seguinte processo:

1. O sistema solicita o nome do usuário. O nome precisa ter no mínimo 3 caracteres.
2. O sistema solicita o e-mail do usuário. O e-mail precisa conter o caractere `@` e a extensão `.com`.
3. O sistema solicita a senha do usuário. A senha precisa ter no mínimo 8 caracteres.

Após as validações, a senha é criptografada utilizando o algoritmo bcrypt, e os dados do usuário (e-mail e senha criptografada) são inseridos na tabela `usuario` do banco de dados. O sistema então exibe uma mensagem de sucesso:


### Funções responsáveis pelo cadastro:

- `is_valid_email(email)`: Valida o formato do e-mail.
- `generate_password_hash(password, method='bcrypt')`: Gera o hash da senha utilizando o algoritmo bcrypt.
- `add_user(username, password)`: Adiciona o usuário no banco de dados.
- `register()`: Função principal que executa o processo de cadastro interativo com o usuário.

## Fluxo de Login

Quando o usuário deseja fazer login, o sistema segue o seguinte processo:

1. O sistema solicita o e-mail do usuário.
2. O sistema verifica se o e-mail existe no banco de dados. Caso o e-mail não exista, uma mensagem de erro é exibida: 
3. Caso o e-mail seja encontrado, o sistema solicita a senha do usuário.
4. A senha fornecida é comparada com o hash armazenado no banco de dados utilizando o bcrypt. Se a senha estiver correta, um token JWT é gerado com validade de 1 dia.
5. O token gerado é armazenado no campo `Token` do usuário no banco de dados.
6. O sistema exibe uma mensagem de boas-vindas ao usuário:


### Funções responsáveis pelo login:

- `login()`: Função principal que executa o processo de login interativo com o usuário.
- `generate_password_hash(password, method='bcrypt')`: Gera o hash da senha utilizando o algoritmo bcrypt.
- `user_has_token(user_email)`: Verifica se o usuário possui um token válido.

## Geração de Token JWT

Durante o login, após a validação da senha, um token JWT é gerado para o usuário. O token contém as seguintes informações:

- `email`: O e-mail do usuário.
- `exp`: A data de expiração do token, que é definida para 1 dia após a geração.

O token JWT é gerado utilizando a chave secreta `secret_key` e o algoritmo `HS256`. O token é então armazenado no banco de dados e pode ser utilizado para autenticar o usuário em futuras requisições.

## Funções Adicionais

- `user_has_token(user_email)`: Verifica se o usuário possui um token válido. Se o token estiver expirado, o sistema solicita que o usuário faça login novamente. Caso o usuário não tenha um token, é exibida a seguinte mensagem:


## Resumo

O processo de cadastro e login envolve as seguintes etapas principais:

1. **Cadastro**: O usuário fornece nome, e-mail e senha, que são validados e armazenados no banco de dados.
2. **Login**: O usuário fornece e-mail e senha, e um token JWT é gerado e armazenado, permitindo acesso autenticado.

O sistema utiliza a criptografia bcrypt para proteger as senhas e o JWT para gerenciar a autenticação de sessão.
