from typing import Dict, List
import config
from modules.asana import task as asana_task


def get_task_notes(client: object,task_gid: str) -> str:
    task: Dict = client.tasks.get_task(task_gid,opt_fields=['html_notes'])
    return task['html_notes']


class AsanaTask:

    '''
    Asana Response:
        'name': 'Feature Requests', 
        'gid': '1200799300000451', 
        'completed': False,   |    True
        'due_on': '2021-12-20'   |   None, 
        'memberships': [{'section': {'gid': '1200799299933142', 'name': 'Overview'}}],     |   []
        'parent': {'gid': '1200799300000451', 'name': 'Feature Requests'},   |   None
        'projects': [{'gid': '1200799299933135', 'name': 'Volkswagen'}],   |   []
        'tags': [{'gid': '1201507444722116', 'name': 'volkswagen'}]    |  []
        'permalink_url': str
    '''

    def __init__(self,asana_response: Dict):
        self.gid: str = asana_response['gid']
        self.name: str = asana_response['name']
        self.url: str   = asana_response['permalink_url'] 
        self.completed:bool = asana_response['completed']
        self.due_on: str = asana_response['due_on']
        self.section: str = None # subtask do not have a section defined
        if (len(asana_response['memberships'])>0):
            self.section: str = asana_response['memberships'][0]['section']
        self.parent: Dict[str,str] = None # only subtasks do have a parent task
        if (asana_response['parent'] != None):
            self.parent = {'gid':asana_response['parent']['gid'],'name':asana_response['parent']['name']}
        self.project: Dict[str,str] = None # subtasks do not have a project defined
        if (len(asana_response['projects']) > 0):
            self.project = {'gid':asana_response['projects'][0]['gid'],'name':asana_response['projects'][0]['name']}
        self.tags: List[str] = []
        for tag in asana_response['tags']:
            self.tags.append(tag['name'])
        self.subtasks = []

    def add_subtask(self,task) -> int:
        self.subtasks.append(task)
        return len(self.subtasks)

    def has_subtask(self,gid: str) -> bool:
        result = False
        for subtask in self.subtasks:
            if subtask.gid == gid:
                result = True
                break
        return result

    def is_subtask(self) -> bool:
        result = None
        if self.is_private():
            result = False
        else:
            #print(f'is_subtask() - {self.parent != None} - {self.project == None} - {(self.parent != None) and (self.project == None)}')
            result = ((self.parent != None) and (self.project == None)) # subtasks do not belong to a project, but do have a parent
        return result

    def is_private(self) -> bool:
        # a private task does not have a project or a parent
        return (self.parent == None and self.project == None)

    def json(self):
        return {'name':self.name,'gid':self.gid,'completed':self.completed,'tags': self.tags, 'url':self.url, 'due_on':self.due_on}

    def __str__(self):
        return f'Task - Name: {self.name} - completed: {self.completed} - gid: {self.gid} - Project: {self.project} - Section: {self.section} - Parent: {self.parent} - Tags: {self.tags} - # subtasks: {len(self.subtasks)}'