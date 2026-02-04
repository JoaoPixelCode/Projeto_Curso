from flask import Flask, Blueprint, jsonify
from sqlalchemy import text
from Banco.database import db

app = Flask(__name__)

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')



# FUNÇÃO DE CONTAGEM

def contar_leads(where=None, params=None):
    base_sql = "SELECT COUNT(*) as total FROM leads"

    if where:
        base_sql += f" WHERE {where}"

    result = db.session.execute(
        text(base_sql),
        params or {}
    ).fetchone()

    return result.total


# ROTAS DO DASHBOARD

@dashboard.route("/quantidade_leads", methods=["GET"])
def quantidade_leads():
    total = contar_leads()

    return jsonify({
        "total_leads": total
    })


@dashboard.route("/quantidade_leads_ativos", methods=["GET"])
def quantidade_leads_ativos():
    total = contar_leads(
        "status = :status",
        {"status": True}
    )

    return jsonify({
        "total_leads": total
    })


@dashboard.route("/quantidade_leads_desativados", methods=["GET"])
def quantidade_leads_desativados():
    total = contar_leads(
        "status = :status",
        {"status": False}
    )

    return jsonify({
        "total_leads": total
    })


@dashboard.route("/quantidade_scoreMax", methods=["GET"])
def quantidade_scoreMax():
    total = contar_leads(
        "score = :score",
        {"score": 100}
    )

    return jsonify({
        "total_leads": total
    })


@dashboard.route("/quantidade_scoreMin", methods=["GET"])
def quantidade_scoreMin():
    total = contar_leads(
        "score = :score",
        {"score": 50}
    )

    return jsonify({
        "total_leads": total
    })

@dashboard.route("/quantidade_cadastros_email", methods=["GET"])
def quantidade_cadastros_email():
    total = contar_leads(
        "email is not NULL AND email != ''",None
    )

    return jsonify({
        "total_leads": total
    })

@dashboard.route("/quantidade_cadastros_telefones", methods=["GET"])
def quantidade_cadastros_telefones():
    total = contar_leads(
        "telefone is not NULL AND telefone != ''",None
    )

    return jsonify({
        "total_leads": total
    })

@dashboard.route("/quantidade_leads_usuario", methods=["GET"])
def quantidade_leads_usuario():

    sql = text("""
        SELECT u.nome AS nome_usuario, COUNT(l.id) AS total_leads
        FROM leads l
        JOIN users u ON u.id = l.user_id
        GROUP BY u.nome
    """)

    result = db.session.execute(sql).fetchall()

    dados = []

    for row in result:
        dados.append({
            "nome_usuario": row.nome_usuario,
            "total_leads": row.total_leads
        })

    return jsonify(dados)


@dashboard.route("/quantidade_leads_full_usuario", methods=["GET"])
def quantidade_leads_full_usuario():

    sql = text("""
        SELECT 
            u.nome AS nome_usuario,
            COUNT(l.id) AS total_leads
        FROM leads l
        JOIN users u ON u.id = l.user_id
        WHERE l.telefone IS NOT NULL 
          AND l.telefone != '' AND l.email IS NOT NULL AND l.email != ''
        GROUP BY u.nome
    """)

    result = db.session.execute(sql).fetchall()

    dados = []

    for row in result:
        dados.append({
            "nome_usuario": row.nome_usuario,
            "total_leads": row.total_leads
        })

    return jsonify(dados)
