# API de Gestão de Leads e Inteligência de Vendas

API REST desenvolvida em **Flask** e **PostgreSQL** para gerenciar o ciclo de vida de leads, integrar uma base de produtos e fornecer métricas para um dashboard de vendas.

**API em produção:** [https://projeto-curso.onrender.com](https://projeto-curso.onrender.com)

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

### Dashboard — Leads
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/dashboard/metrics` | Resumo geral (`?tipo=leads`, `?tipo=score`, `?tipo=vendas`) |
| GET | `/dashboard/quantidade_leads` | Total de leads |
| GET | `/dashboard/quantidade_leads_ativos` | Leads ativos |
| GET | `/dashboard/quantidade_leads_desativados` | Leads desativados |
| GET | `/dashboard/quantidade_scoreMax` | Leads com score 100 |
| GET | `/dashboard/quantidade_scoreMin` | Leads com score 50 |
| GET | `/dashboard/quantidade_cadastros_email` | Percentual de leads com email |
| GET | `/dashboard/quantidade_cadastros_telefones` | Percentual de leads com telefone |
| GET | `/dashboard/criados_do_dia` | Leads criados hoje |
| GET | `/dashboard/criados_em_sete_dias` | Leads dos últimos 7 dias |
| GET | `/dashboard/crescimento_mensal` | Leads por mês |

### Dashboard — Usuários
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/dashboard/ranking` | Top 5 vendedores por volume de leads |
| GET | `/dashboard/media_score_max` | Percentual de leads score 100 por vendedor |
| GET | `/dashboard/quantidade_leads_usuario` | Total de leads por vendedor |
| GET | `/dashboard/quantidade_leads_full_usuario` | Leads completos (email+telefone) por vendedor |

### Dashboard — Produtos
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/dashboard/produtos/mais_vendido` | Produto com mais leads associados |
| GET | `/dashboard/produtos/ranking` | Ranking de produtos por leads e receita |
| GET | `/dashboard/produtos/sem_leads` | Produtos sem nenhum lead associado |
| GET | `/dashboard/relatorio` | Relatório cruzado produto x lead x vendedor (`?tipo=produtos`, `?tipo=vendedores`, `?tipo=geral`) |
