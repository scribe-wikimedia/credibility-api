from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import json
from bson.json_util import dumps

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'references'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/references'

mongo = PyMongo(app)



@app.route('/test', methods=['GET'])
def get_landing():
    """ testing landing page
    :return:
    """
    return jsonify({'result': "This is the landing page of the Credibility API"})

@app.route('/all', methods=['GET'])
def get_all():
    """ Get all data from the database
    :return:
    """
    references = mongo.db.all
    output = []
    for reference in references.find():
        data = {}
        if 'title' in reference:
            data['title'] = reference['title']
        data.update({'page': reference['page'], 'qid': reference['qid'], 'url': reference['url'],
                    'url_domain': reference['url_domain']})
        output.append(data)
    return jsonify({'result': output})


@app.route('/api/<query>', methods=['GET'])
def get_query(query):
    """ Return result for any mongodb find query
    :param query: mongodb query, prefixed with query=
    :return:
    """
    parsed_query = json.loads(query.replace('query=', ''))
    print(parsed_query)
    references = mongo.db.all
    query_result = references.find(parsed_query)

    if query_result:
        output = json.loads(dumps(query_result))
    else:
        output = "This query yields no results"
    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True)