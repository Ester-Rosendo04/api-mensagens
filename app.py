from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate

app = Flask(__name__)

db = SQLAlchemy()

# Configuração do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))

#Caminho do banco de dados dentro do repositório
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "mensagens.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados e o Flask-Migrate
db.init_app(app)  # Inicializa o SQLAlchemy com a aplicação Flask
migrate = Migrate(app, db)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {"id": self.id, "conteudo": self.conteudo}

@app.route("/mensagens", methods=["POST"])
def criar_mensagem():
    data = request.get_json()
    nova_mensagem = Mensagem(conteudo=data["conteudo"])
    db.session.add(nova_mensagem)
    db.session.commit()
    return jsonify(nova_mensagem.to_dict()), 201

@app.route("/mensagens", methods=["GET"])
def listar_mensagens():
    mensagens = Mensagem.query.all()
    return jsonify([m.to_dict() for m in mensagens])

@app.route("/mensagens/<int:id>", methods=["GET"])
def obter_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id)
    return jsonify(mensagem.to_dict())

@app.route("/mensagens/<int:id>", methods=["PUT"])
def atualizar_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id)
    data = request.get_json()
    mensagem.conteudo = data["conteudo"]
    db.session.commit()
    return jsonify(mensagem.to_dict())

@app.route("/mensagens/<int:id>", methods=["DELETE"])
def deletar_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id)
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify({"mensagem": "Mensagem deletada com sucesso."})

# Execução do aplicativo
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados, se não existirem
    app.run(debug=True)
