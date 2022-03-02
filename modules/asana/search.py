
from typing import Dict, List
from modules.asana import task as asana_task


def search_tasks(client: object,workspace_gid: str, project_gids: str,assignee:str,text: str):
    result = []
    tasks: List[Dict]  = client.tasks.search_tasks_for_workspace(workspace_gid, {'text':text,'projects.any':[project_gids]},opt_fields=['name','assignee.email'],limit=100)
    for task in tasks:
        if task['assignee'] != None and task['assignee']['email'] == assignee:
            result.append(task['gid'])
    return result

