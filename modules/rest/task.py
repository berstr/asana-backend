import os
from typing import Dict, List
import config
from modules.asana import task as asana_task


def get_task_notes(request, task_gid:str):
    notes:str = asana_task.get_task_notes(config.ASANA['client'],task_gid)
    result = { 'result' : 'ok', 'notes' : notes }
    return result
