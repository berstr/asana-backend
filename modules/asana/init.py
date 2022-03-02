
from typing import  List
from modules.asana import project as asana_project
from modules.asana import section as asana_section
from modules.asana import tasks as asana_tasks
from modules.asana import task as asana_task



def asana_init(client, workpsace_gid: str, username: str) -> List[asana_project.AsanaProject]:
    tasks: List[asana_task.AsanaTask] = asana_tasks.get_tasks(client, workpsace_gid, username) # get all tasks from Asana that are assigned to the username

    # separate the task list into project top level tasks and subtasks, as well as private tasks:
    top_level_tasks: List[asana_task.AsanaTask] = []
    for task in tasks:
        if (not task.is_subtask()) and (not task.is_private()):
            top_level_tasks.append(task)
    subtasks: List[asana_task.AsanaTask] = []
    for task in tasks:
        if task.is_subtask() == True:
            subtasks.append(task)
    private_tasks: List[asana_task.AsanaTask] = []
    for task in tasks:
        if task.is_private() == True:
            private_tasks.append(task)

    result: List[asana_project.AsanaProject] = []
    for iterator1 in top_level_tasks:
        if asana_project.find_project(result,iterator1.project['gid']) == None:
            project = asana_project.AsanaProject(iterator1.project['name'],iterator1.project['gid'])
            result.append(project)
            for iterator2 in top_level_tasks:
                if (project.gid == iterator2.project['gid']) and (project.has_section(iterator2.section['gid']) == False):
                    section = asana_section.AsanaSection( iterator2.section['name'], iterator2.section['gid'])
                    project.add_section(section)
                    for iterator3 in top_level_tasks:
                        if (section.gid == iterator3.section['gid']):
                            section.add_task(iterator3)
                        for iterator4 in subtasks:
                            if (not iterator3.has_subtask(iterator4.gid)) and (iterator4.parent['gid'] == iterator3.gid):
                                iterator3.add_subtask(iterator4)

    for p in result:
        for s in p.sections:
            for t in s.tasks:
                for st in t.subtasks:
                    pass

    return result

