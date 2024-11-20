import logging


def start_logging():
    logging.basicConfig(filename="logfile.log", format="[%(asctime)s] %(message)s",
                        filemode="w", level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())

def log_actions(fun):
    def wrapper(*args, **kwargs):
        start_logging()
        fun(*args, **kwargs)
        logging.shutdown()
    return wrapper


