from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from uuid import uuid4

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)


def genUUID():
    return str(uuid4().hex)
    

class Pair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100), default=genUUID, nullable=False)
    time_stamp = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return '<Pair %r>' % self.id

@app.route("/", methods=["GET"])
def view():
    new_pair = Pair()
    db.session.add(new_pair)
    db.session.commit()

    obj = {}
    pairs = Pair.query.order_by(desc('time_stamp')).all()
    for pair in pairs:
        obj[str(pair.time_stamp)] = pair.value
    return jsonify(obj)

if __name__ == '__main__':
    app.run()