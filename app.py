from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensagens.db'
db = SQLAlchemy(app)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {"id": self.id, "conteudo": self.conteudo}

# Criando o banco de dados
with app.app_context():
    db.create_all()

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
