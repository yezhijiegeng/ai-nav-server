from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:123456@localhost:3306/ai_navigation"
db = SQLAlchemy(app)

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "url": self.url}

db.create_all()

@app.route("/websites", methods=["GET", "POST"])
def websites():
    if request.method == "GET":
        websites = Website.query.all()
        return jsonify([website.to_dict() for website in websites])
    elif request.method == "POST":
        new_website = Website(name=request.json["name"], url=request.json["url"])
        db.session.add(new_website)
        db.session.commit()
        return jsonify(new_website.to_dict()), 201

@app.route("/websites/<int:website_id>", methods=["GET", "PUT", "DELETE"])
def website(website_id):
    website = Website.query.get_or_404(website_id)
    if request.method == "GET":
        return jsonify(website.to_dict())
    elif request.method == "PUT":
        website.name = request.json["name"]
        website.url = request.json["url"]
        db.session.commit()
        return jsonify(website.to_dict())
    elif request.method == "DELETE":
        db.session.delete(website)
        db.session.commit()
        return "", 204

if __name__ == "__main__":
    app.run(debug=True)