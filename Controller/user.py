from flask import Flask,Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from datetime import date

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
    matricula = request.form.get("matricula") or request.args.get("matricula")

    valido, erro = validador_usuario.ValidadorEmail(email)
    valido, erro = validador_usuario.ValidadorSenha(senha, senha2)
    valido, erro = validador_usuario.ValidadorTelefone(telefone)
    
    if not valido:
        return jsonify({'erro': erro}), 400
    # SQL
    ativo=(True)
    data_criacao = date.today()
    matricula = validador_usuario.gerarMatricula(matricula)
    sql = text("INSERT INTO users (nome, email, telefone, senha, data_criacao,ativo, matricula) VALUES (:nome, :email, :telefone, :senha, :data_criacao, :ativo, :matricula)")
    dados = {"nome": nome, "email": email, "telefone": telefone, "senha": senha, "data_criacao": data_criacao, "ativo": ativo, "matricula": matricula}
    
    result = db.session.execute(sql, dados)
    db.session.commit()  
    return f"Criado com sucesso {nome}, {email}, {telefone}, {senha}, {data_criacao} e {ativo}, e {senha2}, {matricula}"

@usuario.route("/all")
def get_ALL(): 
    sql_query = text("SELECT * FROM users")
    try:
        # result sem dados
        result = db.session.execute(sql_query)
        
        relatorio = result.mappings().all()
        json = [dict(row) for row in relatorio]  # Gambi pq cada linha é um objeto
        
        return json
    except Exception as e:
        return str(e)
    


@usuario.route("/<matricula>", methods=["POST"]) 
def get_one(matricula): 
    sql_query = text("SELECT * FROM users where matricula = :matricula ")
    dados = {"matricula": matricula}

    try:
        result = db.session.execute(sql_query,dados)
        # Mapear todas as colunas para a linha
        linha = result.mappings().all()[0]
        print(linha)
        return dict(linha)
    except Exception as e:
        return str(e)
    
@usuario.route("/<id>", methods=["Put"])
def desativar_usuario(id):
    ativo = False

    sql = text("UPDATE users set ativo = :ativo where id = :id")
    dados = {"ativo": ativo, "id": id}

    result = db.session.execute(sql, dados)
    
    linhas_afetadas = result.rowcount
    
    if linhas_afetadas == 1:
        db.session.commit()
        return f"Cliente com o {id} desativado"
    else:
        db.session.rollback()
        return f"Só deus na causa"  
    
@usuario.route("/reativar/<id>", methods=["PUT"])
def reativar_usuario(id):
    ativo = True

    sql = text("UPDATE users SET ativo = :ativo WHERE id = :id")
    dados = {"ativo": ativo, "id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount

    if linhas_afetadas == 1:
        db.session.commit()
        return f"Cliente com o id {id} foi reativado com sucesso!"
    else:
        db.session.rollback()
        return f"Nenhum usuário encontrado com id {id}, reativação não efetuada."
    
@usuario.route("/atualizar/<id>", methods=["PUT"])
def atualizar(id):
    # captura dados (form-data ou query params ?nome=…&email=…)
    nome = request.form.get("nome") or request.args.get("nome")
    email = request.form.get("email") or request.args.get("email")
    telefone = request.form.get("telefone") or request.args.get("telefone")
    senha = request.form.get("senha") or request.args.get("senha")
    senha2 = request.form.get("senha2") or request.args.get("senha2")

    valido, erro = validador_usuario.ValidadorEmail(email)
    valido, erro = validador_usuario.ValidadorSenha(senha, senha2)
    valido, erro = validador_usuario.ValidadorTelefone(telefone)
    
    if not valido:
        return jsonify({'erro': erro}), 400
    # SQL

    sql = text("UPDATE users SET nome = :nome,email = :email,telefone = :telefone,senha = :senha WHERE id = :id")

    dados = {"nome": nome,"email": email,"telefone": telefone,"senha": senha,"id": id}

    result = db.session.execute(sql, dados)
    linhas_afetadas = result.rowcount

    if linhas_afetadas == 1:
        db.session.commit()
        return f"Usuário com id {id} atualizado!"
    else:
        db.session.rollback()
        return "Erro ao atualizar o usuário", 400
