import sys
import json
import logging

from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer
from tornado.options import define, options 


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s',
                    datefmt='%a-%d-%b-%Y %H:%M:%S',
                    filename='log/etc.log',
                    filemode='w')


define('config', default='./conf/etc.conf', help='Configure, should be json format')


class BasicConnection(object):
    """
    Basic Connection data
    """
    def __init__(self, stream, addr):
        self.__stream = stream
        self.__addr = addr


class ConnectionPool(object):
    """
    Connection Pool
    """
    pool = set()

    @classmethod
    def add_connection(cls, conn):
        """
        Add connection to pool
        """
        cls.pool.add(conn)


class StreamHandler(TCPServer):
    """
    Process incoming connections
    """
    def handle_stream(self, stream, addr):
        """
        Handle stream
        """
        logging.info("new connection from %s", str(addr))
        ConnectionPool.add(BasicConnection(stream, addr))


class ETCServer(object):
    """
    ETC Server implemention
    """
    def __init__(self, config):
        self.__config = config
        self.__server = StreamHandler()

    def start(self):
        """
        Start etc server running
        """
        logging.info('start etc server running')
        self.__server.bind(self.__config['port'])
        self.__server.start()

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

    IOLoop.current().start()

    etc_server.join()
    return 0


if __name__ == '__main__':
    main(sys.argv[1:])
