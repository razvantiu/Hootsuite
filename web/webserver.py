import json

from flask import Flask, jsonify, request
from pymongo import MongoClient

import settings


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {'message': self.message}


app = Flask(__name__)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/items", methods=['GET'])
def web_server():
    missing_error_template = '{} query parameter is missing'
    subreddit = request.args.get('subreddit')
    if not subreddit:
        raise InvalidUsage(missing_error_template.format('subreddit'))

    from_ = request.args.get('from')
    if not from_:
        raise InvalidUsage(missing_error_template.format('from'))

    to = request.args.get('to')
    if not to:
        raise InvalidUsage(missing_error_template.format('to'))

    try:
        from_ = float(from_)
        to = float(to)
    except ValueError, TypeError:
        raise InvalidUsage('Invalid type for from or to parameters')

    # create a MongoConnection
    mongo_client = MongoClient(settings.database_ip, settings.database_port)
    database = mongo_client[settings.database_name]
    query = {
        'subreddit': subreddit,
        'timestamp': {'$gte': from_,
                      '$lte': to}
    }

    # add filter functionality
    keyword = request.args.get('keyword')
    if keyword:
        query.update({
            '$text': {
                '$search': keyword
            }
        })

    results = []
    for submission in database.submission.find(query).sort('timestamp'):
        results.append(submission)

    for comment in database.comment.find(query).sort('timestamp'):
        results.append(comment)

    # close connection
    mongo_client.close()

    results = sorted(results, key=lambda x: x['timestamp'], reverse=True)
    db_result = {subreddit: results}
    return json.dumps(db_result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
