
from typing import Dict, List
from modules.asana import task as asana_task

def get_tasks(client: object,workspace_gid: str, assigne: str) -> List[asana_task.AsanaTask]:
    result = []
    tasks: List[Dict]  = client.tasks.get_tasks({'workspace':workspace_gid,'assignee':assigne},opt_fields=['name','completed','projects.name','projects.gid','memberships.section.name','parent.name','tags.name','due_on','permalink_url'],limit=100)
    for task in tasks:
        result.append(asana_task.AsanaTask(task))
    return result

