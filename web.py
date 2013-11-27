from flask import Flask, jsonify
from models import db


app = Flask(__name__)


#
# routes
#

@app.route('/device/<device_id>')
def device(device_id):
    subscriber = db.Subscriber.one({'id': device_id}, {'_id': False})
    subscriber['followed_bills'] = subscriber.followed_bills()
    subscriber['followed_committees'] = subscriber.followed_committees()
    subscriber['followed_legislators'] = subscriber.followed_legislators()
    return jsonify(subscriber)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
