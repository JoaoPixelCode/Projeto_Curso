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
    sql = text("""
        SELECT 
        ROUND(
        AVG(CASE WHEN email IS NOT NULL AND email != '' THEN 1 ELSE 0 END) * 100,2) AS percentual_email,
        COUNT(CASE WHEN email IS NOT NULL AND email != '' THEN 1 END) AS total_emails
        FROM leads
    """)

    result = db.session.execute(sql).fetchone()

    return jsonify({
        "percentual_leads_com_email": round(float(result[0]), 2),
        "total_leads_com_email": result[1]
    })

@dashboard.route("/quantidade_cadastros_telefones", methods=["GET"])
def quantidade_cadastros_telefones():

    sql = text("""
        SELECT 
        ROUND(
        AVG(CASE WHEN telefone IS NOT NULL AND telefone != '' THEN 1 ELSE 0 END) * 100,2) AS percentual_email,
        COUNT(CASE WHEN telefone IS NOT NULL AND telefone != '' THEN 1 END) AS total_telefones
        FROM leads
    """)

    result = db.session.execute(sql).fetchone()

    return jsonify({
        "percentual_leads_com_Telefone": round(float(result[0]), 2),
        "total_leads_com_telefone": result[1]
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
        SELECT u.nome AS nome_usuario,COUNT(l.id) AS total_leads
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

@dashboard.route("/criados_do_dia", methods=["GET"])
def criados_do_dia():
    sql = text("""
        SELECT COUNT(*) AS total
        FROM leads
        WHERE DATE(data_criacao) = CURRENT_DATE
    """)

    result = db.session.execute(sql).fetchone()

    return jsonify({
        "total_leads": result.total
    })

@dashboard.route("/criados_em_sete_dias", methods=["GET"])
def criados_em_sete_dias():
    sql = text("""
        SELECT COUNT(*) AS total
        FROM leads
        WHERE DATE(data_criacao) >= CURRENT_DATE - INTERVAL '7 days'
    """)

    result = db.session.execute(sql).fetchone()

    return jsonify({
        "total_leads": result.total
    })

@dashboard.route("/crescimento_mensal", methods=["GET"])
def crescimento_mensal():
    sql = text("""
        SELECT DATE_TRUNC('month', data_criacao) AS mes, COUNT(*) AS total
        FROM leads
        GROUP BY mes
        ORDER BY mes
    """)

    result = db.session.execute(sql).fetchall()

    dados = []

    for row in result:
        dados.append({
            "mes": row.mes.strftime("%Y-%m"),
            "total_leads": row.total
        })

    return jsonify(dados)

@dashboard.route("/ranking", methods=["GET"])
def ranking():
    sql = text("""
        SELECT u.nome, COUNT(l.id) AS total
        FROM leads l
        JOIN users u ON u.id = l.user_id
        GROUP BY u.nome
        ORDER BY total DESC
        LIMIT 5
    """)

    result = db.session.execute(sql).fetchall()

    dados = []

    for contador, row in enumerate(result, start =1 ):
        dados.append({
            "posicao": contador,
            "nome": row.nome,
            "total_leads": row.total
        })

    return jsonify(dados)


@dashboard.route("/media_score_max", methods=["GET"])
def media_score_max():
    sql = text("""
      SELECT u.nome, AVG(CASE WHEN l.score = 100 THEN 1 ELSE 0 END) * 100 AS media_score
    FROM leads l
    JOIN users u ON u.id = l.user_id
    GROUP BY u.nome


    """)

    result = db.session.execute(sql).fetchall()

    dados = []

    for row in result:
        dados.append({
            "nome": row.nome,
            "percentual_score_100": round(float(row.media_score), 2)
        })

    return jsonify(dados)

