from flask import Flask, Response, request
from flask_cors import CORS
import json
import jsonpickle
from get_tasks import get_tasks, get_latest_comments
from classify_text import classify_text

app = Flask(__name__)
CORS(app)


@app.route('/api/tasks', methods=['GET'])
def get_tasks_api():
    response = {
        'status': 'fail'
    }
    status_code = 400
    task_type = request.args.get('task_type')  # reddit_classify
    subtask_type = request.args.get('subtask_type')  # toxic_hl
    source = request.args.get('source') # amitheasshole
    limit = int(request.args.get('limit'))
    offset = int(request.args.get('offset'))
    prevIds = request.args.get('prevIds')
    if prevIds:
        prevIds = json.loads(prevIds)
        prevIds = [int(id) for id in prevIds]
    limit = min(limit, 200)
    response = get_latest_comments(source, task_type, subtask_type, limit, offset, prevIds)
    status_code = 200
    response = jsonpickle.encode(response)
    return Response(response=response,
                    status=status_code,
                    mimetype='application/json',
                    headers={'Access-Control-Allow-Credentials': 'true'})

@app.route('/api/classify', methods=['GET'])
def classify():
    text = request.args.get('text')
    response = {
        'status': 'fail',
    }
    status_code = 400
    if text and len(text) > 0:
        response = classify_text(text)
        status_code = 200
    response = jsonpickle.encode(response)
    return Response(response=response,
                    status=status_code,
                    mimetype='application/json',
                    headers={'Access-Control-Allow-Credentials': 'true'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
