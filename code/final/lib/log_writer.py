from lib.utils_common import create_dir_if_not_exists
from lib.utils_common import get_current_timestamp_string


def get_default_logfile(logdir="./logs"):
    # logdir = "./logs"
    create_dir_if_not_exists(logdir)
    logfile = logdir + "/log.txt"
    return logfile


def write_log(message, logdir="./logs", logfile=None):
    if logfile is None:
        logfile = get_default_logfile(logdir)
    timestamp = get_current_timestamp_string()
    with open(logfile, 'a') as log_file:
        log_file.write(
            timestamp + " -- " + str(message) + '\n')
