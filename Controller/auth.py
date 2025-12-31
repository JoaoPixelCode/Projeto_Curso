from flask import Flask,Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

from Banco.database import db
from Classes.usuarios_class import validador_usuario

app = Flask(__name__)
auth= Blueprint('auth', __name__, url_prefix='/auth/')

@auth.route("register", methods=["POST"])
def register():
    # dados que vieram (aceita form ou query params)
    nome = request.form.get("nome") or request.args.get("nome")
    email = request.form.get("email") or request.args.get("email")
    telefone = request.form.get("telefone") or request.args.get("telefone")
    senha = request.form.get("senha") or request.args.get("senha")
    data_criacao = request.form.get("data_criacao") or request.args.get("data_criacao")
    ativo = request.form.get("ativo") or request.args.get("ativo")
    senha2 = request.form.get("senha2") or request.args.get("senha2")
    valido, erro = validador_usuario.ValidadorEmail(email)
    matricula = 0
    if not valido:
        return jsonify({'erro': erro}), 400
    valido, erro = validador_usuario.ValidadorSenha(senha, senha2)
    if not valido:
        return jsonify({'erro': erro}), 400
    valido, erro = validador_usuario.ValidadorTelefone(telefone)
    if not valido:
        return jsonify({'erro': erro}), 400
    # SQL
    senha_hash = generate_password_hash(senha)
    ativo=(True)
    data_criacao = date.today()
    matricula = validador_usuario.gerarMatricula(matricula)
    sql = text("INSERT INTO users (nome, email, telefone, senha, data_criacao,ativo, matricula) VALUES (:nome, :email, :telefone, :senha, :data_criacao, :ativo, :matricula)")
    dados = {"nome": nome, "email": email, "telefone": telefone, "senha": senha_hash, "data_criacao": data_criacao, "ativo": ativo, "matricula": matricula}
    
    result = db.session.execute(sql, dados)
    db.session.commit()  
    return f"Criado com sucesso!"

@auth.route("login", methods=["POST"])
def login():
    
    email = request.form.get("email") or request.args.get("email")
    senha = request.form.get("senha") or request.args.get("senha")

    if not email or not senha:
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
    
    sql = text("SELECT email,senha,ativo,nome FROM users where email=:email")
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

#Dá para melhorar as coisas do mês 1, quando começar o mês dar uma olhda de novo no codigo
# 
# 
# #

