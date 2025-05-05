import logging

LOG_PATH = "./logger/log.txt"

__all__ = [
	'debug',
	'info',
	'warning',
	'error',
	'critical'
]

'''
    Check Path and File existence
'''
import os
# Folders
if os.path.exists('./logger') == False:
    os.makedirs('./logger')
# Files
if os.path.exists("./logger/log.txt") == False:
    with open("./logger/log.txt","w") as f:
    	f.write("")


""" Init
"""

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.DEBUG)
handler = logging.FileHandler(LOG_PATH)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
 
console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)


""" API
"""

def console_level(con):
	'''con: DEBUG,INFO,WARNING,ERROR,CRITICAL
	'''
	console.setLevel(eval('logging.'+con))

def debug(text,LOG_MODULE="Unset"):
	logger.debug(LOG_MODULE+' - '+text)

def info(text,LOG_MODULE="Unset"):
	logger.info(LOG_MODULE+' - '+text)

def warning(text,LOG_MODULE="Unset"):
	logger.warning(LOG_MODULE+' - '+text)

def error(text,LOG_MODULE="Unset"):
	logger.error(LOG_MODULE+' - '+text)

def critical(text,LOG_MODULE="Unset"):
	logger.critical(LOG_MODULE+' - '+text)

