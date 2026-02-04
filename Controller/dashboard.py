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

dashboard.route("/quantidade_cadastros_telefone", methods=["GET"])
def quantidade_cadastros_telefone():
    total = contar_leads(
        "telefone is not NULL AND telefone != ''",None
    )

    return jsonify({
        "total_leads": total
    })