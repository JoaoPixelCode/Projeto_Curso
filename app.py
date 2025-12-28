from flask import Flask
from Banco.database import init_db

app = Flask(__name__)

init_db(app)

if __name__ == "__main__":
    app.run(debug=True)