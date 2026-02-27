from flask import Flask,Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

from Banco.database import db
from Classes.usuarios_class import validador_usuario

app = Flask(__name__)
leads= Blueprint('leads', __name__, url_prefix='/lead/')

@leads.route("", methods=["POST"])
@jwt_required()
def register():
    nome = request.form.get("nome") or request.args.get("nome")
    email = request.form.get("email") or request.args.get("email")
    telefone = request.form.get("telefone") or request.args.get("telefone")
    data_criacao = request.form.get("data_criacao") or request.args.get("data_criacao")
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
    user_id = get_jwt_identity()
    status= True
    data_criacao = date.today()
    sql = text("INSERT INTO leads (nome, email, telefone, status, data_criacao,score,user_id,produto_id) VALUES (:nome, :email, :telefone, :status, :data_criacao, :score, :user_id, :produto_id)")
    dados = {"nome": nome, "email": email, "telefone": telefone, "status": status, "data_criacao": data_criacao, "score": score,"user_id": user_id, "produto_id": produto_id}
    
    result = db.session.execute(sql, dados)
    db.session.commit()  
    return f"Criado com sucesso!"

@leads.route("/all")
@jwt_required()
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
@jwt_required()
def desativar_usuario(id):
    status = False
    sql = text("UPDATE leads set status = :status where id = :id")
    dados = {"status": status, "id": id}

    result = db.session.execute(sql, dados)
    
    linhas_afetadas = result.rowcount
    
    if linhas_afetadas == 1:
        db.session.commit()
        return f"Lead com o {id} desativado"
    else:
        db.session.rollback()
        return f"Só deus na causa"  
    
@leads.route("/reativar/<id>", methods=["PUT"])
@jwt_required()
def reativar_usuario(id):
    status = True

    sql = text("UPDATE leads SET status = :status WHERE id = :id")
    dados = {"status": status, "id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount

    if linhas_afetadas == 1:
        db.session.commit()
        return f"Lead com o id {id} foi reativado com sucesso!"
    else:
        db.session.rollback()
        return f"Nenhum usuário encontrado com id {id}, reativação não efetuada."
    
@leads.route("/atualizar/<id>", methods=["PUT"])
@jwt_required()
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
    
@leads.route("/<id>", methods=["DELETE"])
@jwt_required()
def deletar_lead(id):
    sql = text("DELETE FROM leads WHERE id = :id")
    dados = {"id": id}

    result = db.session.execute(sql, dados)
    linhas_afetadas = result.rowcount

    if linhas_afetadas == 1:
        db.session.commit()
        return jsonify({"msg": f"Lead com id {id} deletado com sucesso!"})
    else:
        db.session.rollback()
        return jsonify({"erro": "Lead não encontrado"}), 404



