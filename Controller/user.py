from flask import Flask,Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

from Banco.database import db
from Classes.usuarios_class import validador_usuario

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
    senha2 = request.form.get("senha2") or request.args.get("senha2")

    valido, erro = validador_usuario.ValidadorEmail(email)
    valido, erro = validador_usuario.ValidadorSenha(senha, senha2)
    
    if not valido:
        return jsonify({'erro': erro}), 400
    # SQL
    sql = text("INSERT INTO users (nome, email, telefone, senha, data_criacao,ativo) VALUES (:nome, :email, :telefone, :senha, :data_criacao, :ativo)")
    dados = {"nome": nome, "email": email, "telefone": telefone, "senha": senha, "data_criacao": data_criacao, "ativo": ativo}
    
    result = db.session.execute(sql, dados)
    db.session.commit()  
    return f"Criado com sucesso {nome}, {email}, {telefone}, {senha}, {data_criacao} e {ativo}, e {senha2}"




#   "id": 1,
#    "nome": "João Silva",
#   "email": "joao@empresa.com",
#   "telefone": "51999999999",
#   "senha": "senha",
#   "data_criacao": "2025-01-15"