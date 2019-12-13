import logging

def init_logging():
    log_format  = '%(asctime)-15s %(name)-25s %(levelname)-8s %(message)s'
    formatter   = logging.Formatter(log_format)
    root_logger = logging.getLogger('')
    handler     = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
