from flask import Flask,Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

from Banco.database import db

app = Flask(__name__)
usuario= Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario.route("/", methods=["POST"])
def criar():
    # dados que vieram (aceita form ou query params)
    nome = request.form.get("nome") or request.args.get("nome")
    email = request.form.get("email") or request.args.get("email")
    telefone = request.form.get("telefone") or request.args.get("telefone")
    senha = request.form.get("senha") or request.args.get("senha")
    data_criacao = request.form.get("data_criacao") or request.args.get("data_criacao")
    ativo = request.form.get("ativo") or request.args.get("ativo")
    
    # SQL
    sql = text("INSERT INTO users (nome, email, telefone, senha, data_criacao,ativo) VALUES (:nome, :email, :telefone, :senha, :data_criacao, :ativo)")
    dados = {"nome": nome, "email": email, "telefone": telefone, "senha": senha, "data_criacao": data_criacao, "ativo": ativo}
    
    if '@' in email:
        if len(senha) >= 8:
             # executar consulta
            result = db.session.execute(sql, dados)
            db.session.commit()  
            return f"Criado com sucesso {nome}, {email}, {telefone}, {senha}, {data_criacao} e {ativo}"
        else:
            return f"Porfavor inisira ao menos 8 caracteres"

    else:
        return f"porfavor insira um email valido"




#   "id": 1,
#    "nome": "João Silva",
#   "email": "joao@empresa.com",
#   "telefone": "51999999999",
#   "senha": "senha",
#   "data_criacao": "2025-01-15"