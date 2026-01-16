from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)


# ================= MODELS =================

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "body": self.body
        }


# ================= ROUTES =================

@app.get("/messages")
def get_messages():
    messages = Message.query.all()
    return jsonify([m.to_dict() for m in messages]), 200


@app.post("/messages")
def create_message():
    data = request.json

    message = Message(
        username=data["username"],
        body=data["body"]
    )

    db.session.add(message)
    db.session.commit()

    return jsonify(message.to_dict()), 201


@app.patch("/messages/<int:id>")
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.json

    message.body = data.get("body", message.body)
    db.session.commit()

    return jsonify(message.to_dict()), 200


@app.delete("/messages/<int:id>")
def delete_message(id):
    message = Message.query.get_or_404(id)

    db.session.delete(message)
    db.session.commit()

    return {}, 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)
