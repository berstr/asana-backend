
from flask import request , jsonify
# from flask_cors import CORS

from modules.rest import health as rest_health
from modules.rest import projects as rest_projects
from modules.rest import task as rest_task


import config

config.init()

# CORS(config.APP)

config.LOGGER.info("STARTUP ASANA SERVICE")

@config.APP.route('/')
def index_html():
    return config.APP.send_static_file('index.html')

@config.APP.route('/health')
def health():
    config.LOGGER.info("GET /health - received")
    result = rest_health.health(request)
    config.LOGGER.info("GET /health - result: {}".format(result['result']))
    return jsonify(result)


@config.APP.route('/projects')
def projects():
    with_sections = request.args.get('with_sections')
    with_tasks = request.args.get('with_tasks')
    with_subtasks = request.args.get('with_subtasks')
    config.LOGGER.info(f'GET /projects - received - with_sections: {with_sections} - with_taskss: {with_tasks} - with_subtaskss: {with_subtasks}')
    result = rest_projects.projects(request, with_sections, with_tasks, with_subtasks)
    config.LOGGER.info("GET /projects - result: {}".format(result['result']))
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@config.APP.route('/projects/search')
def project_search():
    project_gids = request.args.get('project_gids')
    text = request.args.get('text')
    config.LOGGER.info(f'GET /project/search - received - project_gids: {project_gids} - text: {text}')
    result = rest_projects.project_search(request, project_gids, text)
    config.LOGGER.info("GET /project/search - result: {}".format(result['result']))
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@config.APP.route('/task/notes')
def task_notes():
    task_gid = request.args.get('task_gid')
    config.LOGGER.info(f'GET /task/notes - received - task_gid: {task_gid} ')
    result = rest_task.get_task_notes(request,task_gid)
    config.LOGGER.info("GET /task/notes - result: {}".format(result['result']))
    response = jsonify(result)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    from waitress import serve
    config.LOGGER.info("STARTUP waitress server on port %s ..." % (config.ASANA_PORT))
    serve(config.APP, host="0.0.0.0", port=config.ASANA_PORT)


