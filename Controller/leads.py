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
    user_id = request.form.get("user_id") or request.args.get("user_id")
    produto_id = request.form.get("produto_id") or request.args.get("produto_id")

    valido, erro = validador_usuario.ValidadorEmail(email, obrigatorio=False)
    if not valido:
        return jsonify({'erro': erro}), 400
    valido, erro = validador_usuario.ValidadorTelefone(telefone, obrigatorio=False)
    if not valido:
        return jsonify({'erro': erro}), 400
    
    valido, erro = validador_usuario.verificarContato(telefone,email)
    if not valido:
        return jsonify({'erro': erro}), 400
    
    valido, erro = validador_usuario.verificarNome(nome)
    if not valido:
        return jsonify({'erro': erro}), 400
    
    score = validador_usuario.definicaoScore(email,telefone)
    
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

@leads.route("/all")
def get_ALL(): 
    sql_query = text("SELECT * FROM leads")
    try:
        # result sem dados
        result = db.session.execute(sql_query)
        
        relatorio = result.mappings().all()
        json = [dict(row) for row in relatorio] 
        
        return json
    except Exception as e:
        return str(e)
    
    
@leads.route("/<id>", methods=["Put"])
def desativar_usuario(id):
    ativo = False
    sql = text("UPDATE leads set ativo = :ativo where id = :id")
    dados = {"ativo": ativo, "id": id}

    result = db.session.execute(sql, dados)
    
    linhas_afetadas = result.rowcount
    
    if linhas_afetadas == 1:
        db.session.commit()
        return f"Lead com o {id} desativado"
    else:
        db.session.rollback()
        return f"Só deus na causa"  
    
@leads.route("/reativar/<id>", methods=["PUT"])
def reativar_usuario(id):
    ativo = True

    sql = text("UPDATE leads SET ativo = :ativo WHERE id = :id")
    dados = {"ativo": ativo, "id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount

    if linhas_afetadas == 1:
        db.session.commit()
        return f"Lead com o id {id} foi reativado com sucesso!"
    else:
        db.session.rollback()
        return f"Nenhum usuário encontrado com id {id}, reativação não efetuada."
    
@leads.route("/atualizar/<id>", methods=["PUT"])
def atualizar(id):
    nome = request.form.get("nome") or request.args.get("nome")
    email = request.form.get("email") or request.args.get("email")
    telefone = request.form.get("telefone") or request.args.get("telefone")
    

    valido, erro = validador_usuario.ValidadorEmail(email)
    valido, erro = validador_usuario.ValidadorTelefone(telefone)
    
    if not valido:
        return jsonify({'erro': erro}), 400
    # SQL
    score = validador_usuario.definicaoScore(email,telefone)
    sql = text("UPDATE leads SET nome = :nome,email = :email,telefone = :telefone, score = :score WHERE id = :id")

    dados = {"nome": nome,"email": email,"telefone": telefone,"id": id, "score": score}

    result = db.session.execute(sql, dados)
    linhas_afetadas = result.rowcount

    if linhas_afetadas == 1:
        db.session.commit()
        return f"Lead com id {id} atualizado!"
    else:
        db.session.rollback()
        return "Erro ao atualizar o usuário", 400



