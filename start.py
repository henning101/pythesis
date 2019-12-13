import os
import logging
import sys
import webbrowser
import threading
import pythesis.executor as executor 
import pythesis.argparser as argparser
import pythesis.server as server

def init_logging():
    formatter = logging.Formatter('%(asctime)-15s %(name)-25s Line %(lineno)-4s %(levelname)-10s %(message)s')
    args = argparser.args
    logger = logging.getLogger(args.logger)
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    handler.setFormatter(formatter)

    if args.loglevel == 'debug':
        logger.setLevel(logging.DEBUG)
    elif args.loglevel == 'info':
        logger.setLevel(logging.INFO)
    elif args.loglevel == 'warning':
        logger.setLevel(logging.WARNING)
    elif args.loglevel == 'error':
        logger.setLevel(logging.ERROR)
    elif args.loglevel == 'critical':
        logger.setLevel(logging.CRITICAL)
    else:
        argerr()

if __name__ == '__main__':
    argparser.parse_args()
    args = argparser.args
    init_logging()
    logger = logging.getLogger(__name__)
    logger.info('Initializing executor')

    # Initialize the executor:
    executor.init()
    logger.info('Starting Flask server')

    if not(args.debug):
        # Wait a bit, then open the server URL in a web browser:
        if args.host == '0.0.0.0':
            # If the all IP address is used open the localhost URL:
            browser_url = f'http://localhost:{args.port}'
        else:
            browser_url = f'http://{args.host}:{args.port}'
        threading.Timer(1.25, webbrowser.open, [browser_url]).start()

    # Start the Flask server: 
    server.app.run(
        debug=args.debug,
        host=args.host,
        port=args.port
    )
