import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from Banco.database import db
from sqlalchemy import text

produtos = [
    ("CRM Starter", 199.90),
    ("CRM Pro", 499.90),
    ("CRM Enterprise", 1299.90),
    ("Suporte Básico", 99.90),
    ("Suporte Premium", 299.90),
    ("Treinamento Online", 149.90),
    ("Treinamento Presencial", 599.90),
    ("Consultoria 1h", 250.00),
    ("Consultoria 5h", 1100.00),
    ("Consultoria 10h", 2000.00),
    ("Integração API", 799.90),
    ("Relatório Avançado", 349.90),
    ("Dashboard Personalizado", 449.90),
    ("Automação de E-mail", 199.90),
    ("Automação de WhatsApp", 299.90),
    ("Gestão de Tarefas", 129.90),
    ("Pipeline de Vendas", 379.90),
    ("Funil Personalizado", 419.90),
    ("Importação de Leads", 99.90),
    ("Exportação de Dados", 99.90),
    ("Backup Mensal", 49.90),
    ("Backup Semanal", 89.90),
    ("Usuários Extras (5)", 149.90),
    ("Usuários Extras (10)", 249.90),
    ("Armazenamento Extra 10GB", 59.90),
    ("Armazenamento Extra 50GB", 199.90),
    ("Módulo Financeiro", 549.90),
    ("Módulo RH", 499.90),
    ("Módulo Estoque", 399.90),
    ("Módulo Fiscal", 699.90),
    ("App Mobile iOS", 299.90),
    ("App Mobile Android", 299.90),
    ("Painel Multi-empresa", 899.90),
    ("Assinatura Mensal Básica", 79.90),
    ("Assinatura Mensal Pro", 179.90),
    ("Assinatura Anual Básica", 799.90),
    ("Assinatura Anual Pro", 1699.90),
    ("Onboarding Básico", 349.90),
    ("Onboarding Completo", 749.90),
    ("Migração de Dados", 999.90),
    ("Segurança 2FA", 49.90),
    ("Log de Auditoria", 149.90),
    ("Webhook Personalizado", 199.90),
    ("Chatbot de Atendimento", 599.90),
    ("Relatório de Desempenho", 179.90),
    ("Gestão de Contratos", 329.90),
    ("E-mail Marketing", 249.90),
    ("Segmentação de Leads", 219.90),
    ("Plano Família (3 users)", 359.90),
    ("Plano Corporativo (20 users)", 2499.90),
]

def seed():
    with app.app_context():
        for nome, preco in produtos:
            sql = text("INSERT INTO produtos (nome, preco, ativo) VALUES (:nome, :preco, :ativo)")
            db.session.execute(sql, {"nome": nome, "preco": preco, "ativo": True})
        db.session.commit()
        print(f"✅ {len(produtos)} produtos inseridos com sucesso!")

if __name__ == "__main__":
    seed()