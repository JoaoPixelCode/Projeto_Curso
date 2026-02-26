# Projeto_Curso
API de Gestão de Leads e Inteligência de Vendas
API REST desenvolvida em Flask para gerenciar o ciclo de vida de leads, simular uma base de produtos (ERP) e fornecer métricas para um dashboard de vendas.

Como rodar localmente
Pré-requisitos

Python 3.10+
PostgreSQL instalado e rodando

Passo a passo
1. Clone o repositório
bashgit clone https://github.com/seu-usuario/Projeto_Curso.git
cd Projeto_Curso
2. Instale as dependências
bashpip install -r requirements.txt
3. Configure o banco de dados
Crie um banco no PostgreSQL:
sqlCREATE DATABASE projeto_leads;
Crie um arquivo .env na raiz do projeto:
envDATABASE_URL=postgresql+psycopg2://postgres:SUA_SENHA@localhost/projeto_leads
4. Crie as tabelas no banco
Execute no seu PostgreSQL:
sqlCREATE TABLE users (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    senha TEXT NOT NULL,
    data_criacao DATE,
    ativo BOOLEAN DEFAULT TRUE,
    matricula VARCHAR(20)
);

CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco NUMERIC(10, 2) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    status BOOLEAN DEFAULT TRUE,
    score INTEGER,
    data_criacao DATE,
    user_id INTEGER REFERENCES users(id),
    produto_id INTEGER REFERENCES produtos(id)
);
5. Popule os produtos (seeder)
bashpython seeder_produtos.py
6. Rode a aplicação
bashpython app.py
A API estará disponível em: http://localhost:5000

🔑 Autenticação
As rotas protegidas exigem um token JWT. Para obtê-lo:

Crie um usuário em POST /auth/register
Faça login em POST /auth/login
Use o token no header: Authorization: Bearer SEU_TOKEN


📋 Principais rotas
MétodoRotaDescriçãoPOST/auth/registerCadastrar usuárioPOST/auth/loginLogin (retorna JWT)GET/lead/allListar todos os leadsPOST/lead/Criar leadPUT/lead/atualizar/<id>Atualizar leadGET/dashboard/metricsMétricas gerais