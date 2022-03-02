
from modules.asana import task as asana_task

class AsanaSection():
    def __init__(self,name,gid):
        self.name = name
        self.gid = gid
        self.tasks = []

    def add_task(self, task: asana_task.AsanaTask) -> int:
        self.tasks.append(task)
        return len(self.tasks)

    def json(self):
        return {'name': self.name,'gid':self.gid}
        
    def __str__(self):
        return f'name: {self.name} - gid: {self.gid}'