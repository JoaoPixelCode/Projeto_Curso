from flask import Flask
from flask_jwt_extended import JWTManager

from Banco.database import init_db
from Controller.auth import auth
from Controller.leads import leads
from Controller.dashboard import dashboard


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "minha_chave_super_secreta"

jwt = JWTManager(app)

init_db(app)


#BluePrints

app.register_blueprint(auth)
app.register_blueprint(leads)
app.register_blueprint(dashboard)

if __name__ == "__main__":
    app.run(debug=True)