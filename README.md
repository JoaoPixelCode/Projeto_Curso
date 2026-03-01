# API de Gestão de Leads e Inteligência de Vendas

API REST desenvolvida em **Flask** e **PostgreSQL** para gerenciar o ciclo de vida de leads, integrar uma base de produtos e fornecer métricas para um dashboard de vendas.

🌐 **API em produção:** [https://projeto-curso.onrender.com](https://projeto-curso.onrender.com)

---

## Como rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/Projeto_Curso.git
cd Projeto_Curso
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Configure o `.env`**
```env
DATABASE_URL=postgresql+psycopg2://postgres:SUA_SENHA@localhost/projeto_leads
SECRET_KEY=sua-chave-secreta
```

**4. Crie as tabelas no PostgreSQL**
```sql
CREATE DATABASE projeto_leads;

CREATE TABLE users (
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
```

**5. Popule os produtos**
```bash
python seeder_prudutos.py
```

**6. Rode a aplicação**
```bash
python app.py
```

---

## Autenticação

As rotas protegidas exigem token JWT. Para obtê-lo:

1. Crie um usuário em `POST /auth/register`
2. Faça login em `POST /auth/login`
3. Use o token no header: `Authorization: Bearer SEU_TOKEN`

---

## Rotas

### Auth
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/auth/register` | Cadastrar usuário |
| POST | `/auth/login` | Login — retorna JWT |
| GET | `/auth/all` | Listar usuários |
| PUT | `/auth/atualizar/<id>` | Atualizar usuário |
| PUT | `/auth/<id>` | Desativar usuário |
| PUT | `/auth/reativar/<id>` | Reativar usuário |

### Leads
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/lead/` | Criar lead |
| GET | `/lead/all` | Listar leads |
| PUT | `/lead/atualizar/<id>` | Atualizar lead |
| PUT | `/lead/<id>` | Desativar lead |
| PUT | `/lead/reativar/<id>` | Reativar lead |
| DELETE | `/lead/<id>` | Deletar lead |

### Dashboard
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/dashboard/metrics` | Resumo geral (`?tipo=leads`, `?tipo=score`, `?tipo=vendas`) |
| GET | `/dashboard/ranking` | Top 5 vendedores |
| GET | `/dashboard/crescimento_mensal` | Leads por mês |
| GET | `/dashboard/criados_do_dia` | Leads criados hoje |
| GET | `/dashboard/criados_em_sete_dias` | Leads dos últimos 7 dias |
| GET | `/dashboard/quantidade_leads_usuario` | Leads por vendedor |
