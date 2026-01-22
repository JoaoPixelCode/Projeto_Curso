from flask import Flask,Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

from Banco.database import db
from Classes.usuarios_class import validador_usuario

app = Flask(__name__)
leads= Blueprint('leads', __name__, url_prefix='/lead/')

@leads.route("", methods=["POST"])
def register():
    nome = request.form.get("nome") or request.args.get("nome")
    email = request.form.get("email") or request.args.get("email")
    telefone = request.form.get("telefone") or request.args.get("telefone")
    status = request.form.get("status") or request.args.get("status")
    data_criacao = request.form.get("data_criacao") or request.args.get("data_criacao")
    score = request.form.get("score") or request.args.get("score")
    user_id = request.form.get("user_id") or request.args.get("user_id")
    produto_id = request.form.get("produto_id") or request.args.get("produto_id")
    valido, erro = validador_usuario.ValidadorEmail(email)
    ok, erro = validador_usuario.ValidadorTelefone(telefone, obrigatorio=False)

    if not valido:
        return jsonify({'erro': erro}), 400
    valido, erro = validador_usuario.ValidadorTelefone(telefone)
    if not valido:
        return jsonify({'erro': erro}), 400
    
    data_criacao = date.today()
    sql = text("INSERT INTO leads (nome, email, telefone, status, data_criacao,score,user_id,produto_id) VALUES (:nome, :email, :telefone, :status, :data_criacao, :score, :user_id, :produto_id)")
    dados = {"nome": nome, "email": email, "telefone": telefone, "status": status, "data_criacao": data_criacao, "score": score,"user_id": user_id, "produto_id": produto_id}
    
    result = db.session.execute(sql, dados)
    db.session.commit()  
    return f"Criado com sucesso!"

@leads.route("login", methods=["POST"])
def login():
    
    email = request.form.get("email") or request.args.get("email")
    senha = request.form.get("senha") or request.args.get("senha")

    if not email or not senha:
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
    
    sql = text("SELECT email,senha,ativo,nome FROM leads where email=:email")
    dados = {"email":email}

    result =db.session.execute(sql,dados)
    db.session.commit()

    users = result.fetchone()

    if not users:
        return f"Nada encontrado"
    
    if not users.ativo:
        return f"Usuario desativado"
    if check_password_hash(users.senha, senha):
        return f"Login Realizado com suesso! Seja bem vindo {users.nome}"

#Dá para melhorar as coisas do mês 1, quando começar o mês dar uma olhda de novo no codigo principalmente no JWT
# 
# 
# #


