# SQLAlchemy FastAPI REST API

API REST desenvolvida com FastAPI, SQLAlchemy e SQLite para gerenciamento de usuários, produtos e pedidos. A aplicação utiliza autenticação com JWT e dados de acesso protegidos em rotas específicas.

## 📌 Visão geral

Este projeto implementa um backend simples de loja/gestão de pedidos com os seguintes módulos principais:

- autenticação de usuários com login e geração de tokens JWT;
- cadastro e listagem de usuários;
- cadastro, consulta e atualização de produtos;
- criação, consulta e listagem de pedidos com cálculo do valor total;
- persistência em SQLite com ORM SQLAlchemy;
- migrações e versionamento do banco com Alembic.

## 🧰 Stack tecnológica

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Alembic
- Passlib + BCrypt
- python-jose
- python-dotenv

## 🗂️ Estrutura da aplicação

```text
app/
├── main.py                     # aplicação FastAPI e inclusão de rotas
├── core/
│   └── dependencies.py         # criação de sessão e validação JWT
├── database/
│   └── models.py               # modelos ORM do banco de dados
├── routes/
│   ├── auth_routes.py          # cadastro, login e autenticação
│   ├── order_routes.py         # criação/listagem de pedidos
│   └── Products_routes.py      # CRUD de produtos
└── schemas/
    ├── Orders_eschema.py
    ├── Product_eschema.py
    └── Users_eschema.py
```

## ⚙️ Configuração

### Dependências

O projeto depende de bibliotecas como:

```bash
pip install fastapi uvicorn sqlalchemy alembic python-jose passlib bcrypt python-dotenv pydantic
```

O arquivo de requisitos foi incluído como [requeriments.txt](requeriments.txt), porém ainda está vazio e pode ser atualizado com versões fixas conforme a necessidade do ambiente.

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo:

```env
SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Essas variáveis são lidas em [app/main.py](app/main.py) e utilizadas em [app/routes/auth_routes.py](app/routes/auth_routes.py) para assinar e validar tokens JWT.

## 🛢️ Banco de dados

A persistência é feita com SQLite e a conexão é definida em [app/database/models.py](app/database/models.py):

```python
DATABASE_URL = f"sqlite:///{BASE_DIR}/banco.db"
```

As migrações ficam na pasta [alembic](alembic) e a configuração principal do Alembic está em [alembic.ini](alembic.ini).

## 🚀 Executando a API

Para iniciar o servidor em desenvolvimento:

```bash
uvicorn app.main:App --reload
```

A aplicação passa a ficar disponível em:

- http://127.0.0.1:8000

A documentação automática do FastAPI pode ser acessada em:

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc

## 🔐 Endpoints

### Autenticação

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/auth/create_user` | Cria um usuário novo. |
| GET | `/auth/get_user/{usuario_id}` | Busca usuário pelo identificador. |
| GET | `/auth/list_user` | Lista todos os usuários. |
| POST | `/auth/login` | Faz login com `email` e `senha` e retorna access/refresh tokens. |
| POST | `/auth/login-form` | Login compatível com o formato OAuth2 `PasswordRequestForm`. |
| GET | `/auth/refresh` | Gera um novo `access_token` a partir do usuário autenticado. |

### Produtos

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/products/list_products` | Lista os produtos cadastrados. |
| POST | `/products/create_product` | Cria um novo produto. |
| POST | `/products/edit_product/{product_id}` | Atualiza um produto existente. |

### Pedidos

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/order/create_order` | Cria um pedido com uma lista de itens e calcula o `total`. |
| GET | `/order/get_order/{order_id}` | Busca um pedido pelo identificador. |
| GET | `/order/list_order` | Lista todos os pedidos. |

## 🧾 Exemplo de payloads

### Usuário

```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "123456"
}
```

### Login

```json
{
  "email": "joao@email.com",
  "senha": "123456"
}
```

### Produto

```json
{
  "nome": "Notebook",
  "descricao": "Notebook gamer",
  "preco": 2500.00,
  "estoque": 10
}
```

### Pedido

```json
{
  "user_id": 1,
  "itens": [
    {
      "product_id": 1,
      "quantidade": 2
    }
  ]
}
```

## ✅ Observações

- As rotas de produtos e pedidos são acessadas por meio do FastAPI com esquema Pydantic e resposta serializada em JSON.
- A autenticação JWT exige o envio do token via header `Authorization: Bearer <token>` nos fluxos protegidos.
- A aplicação encontra-se em uma etapa inicial/educacional, com endpoints de CRUD básicos e uma base de dados local para testes.
