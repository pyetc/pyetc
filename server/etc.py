import sys
import json
import logging

from tornado.tcpserver import TCPServer
from tornado.options import define, options 


define('config', default='./conf/etc.conf', help='Configure, should be json format')


class ETCServer(TCPServer):
    """
    ETC Server implemention
    """
    def __init__(self, config):
        self.__config = config

    def start(self):
        """
        Start etc server running
        """
        logging.info('start etc server running')

    def join(self):
        """
        Wait until etc server exit
        """
        logging.info('join etc server')


def main(argv):
    """
    Main entry of etc server
    """
    options.parse_command_line()

    try:
        config_file = open(options.config)
        config = json.load(config_file)
        config_file.close()
    except Exception as e:
        print e
        return -1

    etc_server = ETCServer(config)
    etc_server.start()

    etc_server.join()
    return 0


if __name__ == '__main__':
    main(sys.argv[1:])
