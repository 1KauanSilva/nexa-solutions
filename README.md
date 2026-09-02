# Sistema de Chamados — Nexa Solutions

Projeto desenvolvido para a disciplina de **Manutenção e Evolução de Software**. O sistema permite o cadastro, consulta, atualização e acompanhamento de chamados de suporte por meio de uma API REST desenvolvida em Django e de uma interface HTML simples.

## Contexto

A Nexa Solutions possui um sistema interno para abertura e acompanhamento de chamados de suporte.

O projeto disponibiliza uma API REST responsável pelo gerenciamento dos chamados e uma interface HTML simples para interação com o sistema.

A aplicação utiliza **Django REST Framework** para disponibilização da API e **PostgreSQL** como banco de dados no ambiente Docker.

## Tecnologias

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL 16
- Docker
- Docker Compose
- Git

## Estrutura do projeto

```text
nexa-solutions/
├── backend/
│   ├── chamados/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   └── ...
├── docs/
│   └── ...
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── README.md
```

### Principais diretórios

- `backend/`: contém a aplicação Django e a API REST.
- `backend/chamados/`: contém os modelos, serializers, views, URLs e testes relacionados aos chamados.
- `frontend/`: contém a interface HTML do projeto.
- `docs/`: contém documentos e materiais relacionados ao projeto.

## Configuração do ambiente

O projeto utiliza variáveis de ambiente para configurar a aplicação e o banco de dados.

O arquivo `.env.example` contém um modelo das variáveis necessárias para executar o projeto.

Para criar o arquivo `.env`, copie o arquivo de exemplo.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux/macOS

```bash
cp .env.example .env
```

Depois, revise as variáveis do arquivo `.env`.

Exemplo:

```env
DJANGO_SECRET_KEY=troque-esta-chave-em-producao
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=nexa_chamados
POSTGRES_USER=nexa_user
POSTGRES_PASSWORD=troque-esta-senha
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

> **Importante:** o arquivo `.env` pode conter informações sensíveis e não deve ser versionado no repositório. Para ambientes reais, utilize uma chave secreta e uma senha de banco adequadas.

## Execução com Docker

O projeto possui configuração com Docker e Docker Compose para facilitar a reprodução do ambiente de desenvolvimento.

Antes de iniciar, certifique-se de que o **Docker Desktop** esteja em execução.

### Construir e iniciar os containers

Na raiz do projeto, execute:

```bash
docker compose up --build
```

Esse comando cria a imagem da API, inicia o PostgreSQL e inicia a aplicação Django.

Para executar os containers em segundo plano:

```bash
docker compose up -d
```

### Verificar os containers

```bash
docker compose ps
```

O serviço do banco de dados deve apresentar o estado `healthy`.

### Parar os containers

```bash
docker compose down
```

Os dados do PostgreSQL são armazenados em um volume Docker chamado `postgres_data`.

## Execução local

Também é possível executar o backend utilizando um ambiente virtual Python.

Entre no diretório do backend:

```bash
cd backend
```

Crie o ambiente virtual.

### Windows PowerShell

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Depois execute as migrações:

```bash
python manage.py migrate
```

E inicie o servidor:

```bash
python manage.py runserver
```

> Para o ambiente configurado atualmente, a execução com Docker Compose é a forma recomendada, pois fornece o PostgreSQL utilizado pela aplicação.

## Testes

Os testes automatizados estão localizados em:

```text
backend/chamados/tests.py
```

Como o ambiente Docker fornece o banco PostgreSQL configurado para a aplicação, os testes podem ser executados dentro do container da API.

Execute:

```bash
docker compose exec api python manage.py test chamados
```

Um resultado esperado é semelhante a:

```text
Found 3 test(s).
...
Ran 3 tests
OK
```

Os testes verificam comportamentos importantes da aplicação, incluindo a validação de chamados e o funcionamento dos indicadores.

## API

A API está disponível, por padrão, em:

```text
http://localhost:8000/api/
```

### Chamados

#### Listar chamados

```http
GET /api/chamados/
```

Retorna os chamados cadastrados no sistema.

#### Criar chamado

```http
POST /api/chamados/
```

Cria um novo chamado.

O campo `titulo` é obrigatório.

Exemplo de requisição:

```json
{
    "titulo": "Computador não inicia",
    "descricao": "O computador apresenta problema ao iniciar.",
    "status": "ABERTO"
}
```

Caso o título não seja informado ou esteja em branco, a API retorna um erro de validação HTTP 400.

#### Consultar um chamado

```http
GET /api/chamados/<id>/
```

Retorna os dados de um chamado específico.

#### Atualizar um chamado

```http
PUT /api/chamados/<id>/
```

Atualiza os dados de um chamado.

Também é possível realizar atualizações parciais utilizando:

```http
PATCH /api/chamados/<id>/
```

#### Excluir um chamado

```http
DELETE /api/chamados/<id>/
```

Remove um chamado.

### Filtro por status

A listagem de chamados permite filtrar os resultados pelo status.

Utilize o parâmetro `status`:

```http
GET /api/chamados/?status=ABERTO
```

Os status disponíveis são:

```text
ABERTO
EM_ANDAMENTO
CONCLUIDO
```

O filtro também aceita os valores sem depender de letras maiúsculas ou minúsculas.

Caso seja informado um status inválido, a API retorna HTTP 400 e informa os status válidos.

Exemplo:

```json
{
    "detail": "Status inválido.",
    "status_validos": [
        "ABERTO",
        "EM_ANDAMENTO",
        "CONCLUIDO"
    ]
}
```

### Indicadores

A API disponibiliza um endpoint para consulta de indicadores dos chamados:

```http
GET /api/indicadores/
```

O endpoint retorna:

- quantidade total de chamados;
- quantidade de chamados abertos;
- quantidade de chamados em andamento;
- quantidade de chamados concluídos.

Exemplo de resposta:

```json
{
    "total": 10,
    "abertos": 4,
    "em_andamento": 3,
    "concluidos": 3
}
```

## Administração

O Django disponibiliza uma área administrativa em:

```text
http://localhost:8000/admin/
```

O acesso depende de um usuário administrador configurado na aplicação.

## Principais endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/chamados/` | Lista chamados |
| `POST` | `/api/chamados/` | Cria chamado |
| `GET` | `/api/chamados/<id>/` | Consulta um chamado |
| `PUT` | `/api/chamados/<id>/` | Atualiza um chamado |
| `PATCH` | `/api/chamados/<id>/` | Atualiza parcialmente um chamado |
| `DELETE` | `/api/chamados/<id>/` | Exclui um chamado |
| `GET` | `/api/chamados/?status=ABERTO` | Filtra chamados por status |
| `GET` | `/api/indicadores/` | Consulta indicadores |
| — | `/admin/` | Área administrativa do Django |

## Fluxo básico de execução

Para executar o projeto utilizando Docker:

```bash
docker compose up --build
```

Depois, a API poderá ser acessada em:

```text
http://localhost:8000/api/chamados/
```

Para executar os testes:

```bash
docker compose exec api python manage.py test chamados
```

Para encerrar o ambiente:

```bash
docker compose down
```

## Observações

Este projeto faz parte de uma atividade acadêmica de **Manutenção e Evolução de Software**. As funcionalidades e configurações documentadas neste arquivo correspondem ao estado atual do projeto.