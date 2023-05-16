import logging
import os
import datetime

uvLogger = logging.getLogger('uvLogger')
uvLogger.setLevel(logging.DEBUG)

log_dir = 'log'
os.makedirs(log_dir, exist_ok=True)


log_file = 'unicode_viewer.log'  
log_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
log_file_name = f'unicode_viewer_{log_time}.log'
file_handler = logging.FileHandler(os.path.join(log_dir, log_file_name), mode='a', delay=True)
console_handler = logging.StreamHandler()
log_format = '%(asctime)s | %(levelname)s | %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(log_format, datefmt=date_format)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
uvLogger.addHandler(file_handler)
uvLogger.addHandler(console_handler)

def enable_logging():
    uvLogger.setLevel(logging.DEBUG)
def disable_logging():
    uvLogger.setLevel(logging.CRITICAL)
def debug(message):
    uvLogger.debug(message)
def info(message):
    uvLogger.info(message)
def warning(message):
    uvLogger.warning(message)
def error(message):
    uvLogger.error(message)
def critical(message):
    uvLogger.critical(message)
