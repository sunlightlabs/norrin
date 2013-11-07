import uuid

from flask import Flask, jsonify, request
from flask.ext.mongokit import MongoKit
from bson import BSON

from activities import FEED_ACTIVITIES, NOTIFICATION_ACTIVITIES
from models import Activity, Subscriber

# MONGODB_DATABASE = 'flask'
# MONGODB_HOST = 'localhost'
# MONGODB_PORT = 27017
# MONGODB_USERNAME = None
# MONGODB_PASSWORD = None

app = Flask(__name__)


#
# mongodb and mongokit configuration
#

db = MongoKit(app)
db.register([Activity, Subscriber])


#
# routes
#

@app.route('/activities', methods=['GET'])
def list_activities():
    data = {
        'feeds': [a.type for a in FEED_ACTIVITIES],
        'activities': [a.type for a in NOTIFICATION_ACTIVITIES],
    }
    return jsonify(data)


@app.route('/subscribers', methods=['GET'])
def list_subscribers():
    page = int(request.args.get('page', 0))
    per_page = int(request.args.get('per_page', 50))
    subscribers = db.Subscriber.find({}, {'_id': False}).skip(page * per_page).limit(per_page)

    data = {'subscribers': []}

    for s in subscribers:
        subscriber = dict(s)
        subscriber['url'] = '/subscribers/%s' % s.uuid
        data['subscribers'].append(subscriber)

    return jsonify(data)


@app.route('/subscribers', methods=['POST'])
def add_subscriber():
    # subscriber = db.Subscriber()
    # subscriber.uuid = unicode(uuid.uuid4().hex)
    # subscriber.device = unicode(uuid.uuid4().hex)
    # subscriber.timezone = unicode('-04:00')
    # subscriber.favorites = ['l/M000702', 'l/D000620', 'c/HSAS', 'b/hr2775-113']
    # subscriber.save()

    # data = {
    #     'url': '/subscribers/%s' % subscriber.uuid,
    #     'subscriber': subscriber.to_json(),
    # }

    # return jsonify(data)

    return jsonify({})


@app.route('/subscribers/<subscriber_id>')
def subscriber(subscriber_id):
    subscriber = db.Subscriber.one({'uuid': subscriber_id}, {'_id': False})
    subscriber['followed_bills'] = subscriber.followed_bills()
    subscriber['followed_committees'] = subscriber.followed_committees()
    subscriber['followed_legislators'] = subscriber.followed_legislators()
    return jsonify(subscriber)


@app.route('/subscribers/<subscriber_id>/following', methods=['POST', 'DELETE'])
def modify_following(subscriber_id):
    if request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass
    else:
        pass


if __name__ == "__main__":
    app.run(debug=True, port=8000)
