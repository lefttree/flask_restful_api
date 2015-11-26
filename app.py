#!env/bin/python
# -*- coding: utf-8 -*-
"""
Flask app
"""
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/')
def index():
    """
    Index page
    """
    return "Hello, world!"


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    """
    GET method api to get all tasks
    """
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    GET method api to get one specific task
    """
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.errorhandler(404)
def not_found(error):
    """
    404 Error handler
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    """
    PUT method api to create a new task
    """
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    PUT method api to update task
    """
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and not \
            isinstance(request.json['title'], unicode):
        abort(400)
    if 'description' in request.json and not\
            isinstance(request.json['description'], unicode):
        abort(400)
    if 'done' in request.json and not isinstance(request.json['done'], bool):
        abort(400)

    task_to_update = task[0]
    task_to_update['title'] = request.json.get('title',
                                               task_to_update['title'])
    task_to_update['description'] = \
        request.json.get('description', task_to_update['description'])
    task_to_update['done'] = request.json.get('done', task_to_update['done'])
    return jsonify({'task': task_to_update})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    DELETE method api to delete a task
    """
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])

    return jsonify({'result': True})


# --------------------------------------------------------------------------
##
# @Xiang
#
# @Param task
#
# @Returns new_task with 'id' field replace with 'uri'
# ----------------------------------------------------------------------------
def make_public_task(task):
    """
    make public uri for task
    """
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'],
                                      _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@auth.get_password
def get_password(username):
    if username == 'xiang':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

if __name__ == "__main__":
    app.run(debug=True)
