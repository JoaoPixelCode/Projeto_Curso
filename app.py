from flask import Flask
from Banco.database import init_db
from Controller.user import usuario

app = Flask(__name__)

init_db(app)


#BluePrints

app.register_blueprint(usuario)

if __name__ == "__main__":
    app.run(debug=True)