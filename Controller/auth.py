from flask import Flask,Blueprint, request, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity


from Banco.database import db
from Classes.usuarios_class import validador_usuario

app = Flask(__name__)
auth= Blueprint('auth', __name__, url_prefix='/auth/')

@auth.route("register", methods=["POST"])
def register():
    nome = request.form.get("nome") or request.args.get("nome")
    email = request.form.get("email") or request.args.get("email")
    telefone = request.form.get("telefone") or request.args.get("telefone")
    senha = request.form.get("senha") or request.args.get("senha")
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
    ok, erro = validador_usuario.ValidadorTelefone(telefone, obrigatorio=True)
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
    
    sql = text("SELECT id,email,senha,ativo,nome FROM users WHERE email=:email")
    dados = {"email":email}

    result = db.session.execute(sql, dados)
    user = result.fetchone()

    if not user:
        return jsonify({"erro":"Usuário não encontrado"}), 404
    
    if not user.ativo:
        return jsonify({"erro":"Usuário desativado"}), 403

    if not check_password_hash(user.senha, senha):
        return jsonify({"erro": "Senha incorreta"}), 401

    token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "email": user.email,
            "nome": user.nome
        }
    )

    return jsonify({
        "msg": "Login realizado com sucesso",
        "token": token
    })

@auth.route("/all")
@jwt_required()
def get_ALL(): 
    sql_query = text("SELECT * FROM users")
    try:
        # result sem dados
        result = db.session.execute(sql_query)
        
        relatorio = result.mappings().all()
        json = [dict(row) for row in relatorio] 
        
        return json
    except Exception as e:
        return str(e)
    


@auth.route("/matricula/<matricula>", methods=["GET"]) 
def get_one(matricula): 

    sql_query = text("SELECT * FROM users WHERE matricula = :matricula")
    dados = {"matricula": matricula}

    result = db.session.execute(sql_query, dados)

    linha = result.mappings().first()

    if not linha:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return dict(linha)

    
@auth.route("/<id>", methods=["Put"])
def desativar_usuario(id):
    ativo = False
    sql = text("UPDATE users set ativo = :ativo where id = :id")
    dados = {"ativo": ativo, "id": id}

    result = db.session.execute(sql, dados)
    
    linhas_afetadas = result.rowcount
    
    if linhas_afetadas == 1:
        db.session.commit()
        return f"Usuario com o {id} desativado"
    else:
        db.session.rollback()
        return f"Só deus na causa"  
    
@auth.route("/reativar/<id>", methods=["PUT"])
def reativar_usuario(id):
    ativo = True

    sql = text("UPDATE users SET ativo = :ativo WHERE id = :id")
    dados = {"ativo": ativo, "id": id}

    result = db.session.execute(sql, dados)

    linhas_afetadas = result.rowcount

    if linhas_afetadas == 1:
        db.session.commit()
        return f"Usuario com o id {id} foi reativado com sucesso!"
    else:
        db.session.rollback()
        return f"Nenhum usuário encontrado com id {id}, reativação não efetuada."
    
@auth.route("/atualizar/<id>", methods=["PUT"])
def atualizar(id):
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

#Dá para melhorar as coisas do mês 1, quando começar o mês dar uma olhda de novo no codigo principalmente no JWT
# 
# 
# #

