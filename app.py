from flask import Flask
from Banco.database import init_db
from Controller.user import usuario
from Controller.auth import auth
from Controller.leads import leads


app = Flask(__name__)

init_db(app)


#BluePrints

app.register_blueprint(usuario)
app.register_blueprint(auth)
app.register_blueprint(leads)

if __name__ == "__main__":
    app.run(debug=True)