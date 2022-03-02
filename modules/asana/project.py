from typing import List
from modules.asana import section as asana_section

class AsanaProject:
    def __init__(self,name:str,gid:str):
        self.name = name
        self.gid = gid
        self.sections = []
    
    def add_section(self,section: asana_section.AsanaSection) -> int:
        self.sections.append(section)
        return len(self.sections)

    def has_section(self,gid: str) -> bool:
        result: bool = False
        for section in self.sections:
            if section.gid == gid:
                result = True
                break
        return result

    def json(self,with_sections=None, with_tasks=None, with_subtasks=None):
        if (with_sections==None):
            return {'name': self.name,'gid':self.gid}
        else:
            sections = []
            for section in self.sections:
                if (with_tasks==None):
                    sections.append(section.json())
                else:
                    section_json =  section.json()
                    tasks = []
                    for task in section.tasks:
                        if (with_subtasks == None):
                            tasks.append(task.json())
                        else:
                            task_json=task.json()
                            subtasks = []
                            for subtask in task.subtasks:
                                subtasks.append(subtask.json())
                            task_json['subtasks'] = subtasks
                            tasks.append(task_json)
                    section_json['tasks']=tasks
                    sections.append(section_json)
            return {'name': self.name,'gid':self.gid, 'sections':sections}
            

    def __str__(self):
        return f'name: {self.name} - gid: {self.gid}'
    


def find_project(projects: List[AsanaProject], gid: str) -> AsanaProject:
    result: AsanaProject = None
    for project in projects:
        if project.gid == gid:
            result = project
            break
    return result
