from flask import Flask #, jsonify, request

import os
import logging
from newrelic.agent import NewRelicContextFormatter
from logging.handlers import RotatingFileHandler

from modules.asana import login

# ==========================
# Constants
# ==========================
ASANA_PORT_DEFAULT = 37070


# ==========================
# The following variables are being set by the application at runtime:
# ==========================
APP = None
LOGGER = None
ASANA = None
# ASANA_PROJECTS = None


# ==========================
# The following variables are set through env variables
# ==========================


ASANA_USERNAME = os.environ.get("ASANA_USERNAME")
if (ASANA_USERNAME == None):
    print('FATAL - env ASANA_USERNAME not defined - Exit service')
    quit()

ASANA_PERSONAL_TOKEN=os.environ.get("ASANA_PERSONAL_TOKEN")
if (ASANA_PERSONAL_TOKEN == None):
    print('FATAL - env ASANA_PERSONAL_TOKEN not defined - Exit service')
    quit()


ASANA_PORT = os.environ.get("ASANA_PORT")
if (ASANA_PORT == None):
    ASANA_PORT=ASANA_PORT_DEFAULT




# ==========================
# Init of variables, etc.
# ==========================

APP = Flask(__name__,static_folder='public', static_url_path='')


def init():
    init_logger()
    asana_login()

def asana_login():
    global ASANA
    ASANA = login.asana_login(ASANA_PERSONAL_TOKEN)




def init_logger():
    global LOGGER
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler('logs/asana.log', maxBytes=10485760, backupCount=2) # max logfile size: 10MB
    newrelic_formatter = NewRelicContextFormatter()
    file_handler.setFormatter(newrelic_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    LOGGER = logger


