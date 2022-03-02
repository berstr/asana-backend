import os
from ssl import get_protocol_name
import config
from typing import Dict, List

from modules.asana import project as asana_project
from modules.asana import section as asana_section
from modules.asana import tasks as asana_tasks
from modules.asana import task as asana_task
from modules.asana import search as asana_search

import config


def projects(request, with_sections, with_tasks,with_subtasks):
    projects_result = []

    ASANA_PROJECTS = __asana_get_all_tasks(config.ASANA['client'],config.ASANA['workspace']['gid'] ,config.ASANA_USERNAME)
    for project in ASANA_PROJECTS:
        projects_result.append(project.json(with_sections, with_tasks,with_subtasks))
    result = { 'result' : 'ok', 'projects' : projects_result }
    return result

def project_search(request, project_gids, text):
    task_gids = asana_search.search_tasks(config.ASANA['client'],config.ASANA['workspace']['gid'] , project_gids,  config.ASANA_USERNAME, text)
    result = { 'result' : 'ok', 'tasks' : task_gids, 'search': text , 'project_gids': project_gids}
    return result


# custom functions to get employee info
def __get_name(object):
    return object.name




def __asana_get_all_tasks(client, workpsace_gid: str, username: str) -> List[asana_project.AsanaProject]:
    tasks: List[asana_task.AsanaTask] = asana_tasks.get_tasks(client, workpsace_gid, username) # get all tasks from Asana that are assigned to the username

    # separate the task list into project top level tasks and subtasks, as well as private tasks:
    top_level_tasks: List[asana_task.AsanaTask] = []
    for task in tasks:
        if (not task.is_subtask()) and (not task.is_private()):
            top_level_tasks.append(task)
            #print(f'TOP TASK: {task}')
    subtasks: List[asana_task.AsanaTask] = []
    for task in tasks:
        if task.is_subtask() == True:
            subtasks.append(task)
            #print(f'SUB TASK: {task}')
    private_tasks: List[asana_task.AsanaTask] = []
    for task in tasks:
        if task.is_private() == True:
            private_tasks.append(task)
            #print(f'PRIVATE TASK: {task}')

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
                        #print(f'TASK: {iterator3}')
                        if (section.gid == iterator3.section['gid']):
                            section.add_task(iterator3)
                        for iterator4 in subtasks:
                            if (not iterator3.has_subtask(iterator4.gid)) and (iterator4.parent['gid'] == iterator3.gid):
                                iterator3.add_subtask(iterator4)

    result.sort(key=__get_name)

    for projects in result:
        projects.sections.sort(key=__get_name)

    return result
