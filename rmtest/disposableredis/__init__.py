import subprocess
import socket
import tempfile
import redis
import time
import os
import sys
import itertools
from contextlib import contextmanager


def get_random_port():
    sock = socket.socket()
    sock.listen(0)
    _, port = sock.getsockname()
    sock.close()

    return port


class Client(redis.StrictRedis):

    def __init__(self, disposable_redis, port):

        redis.StrictRedis.__init__(self, port = port)
        self.dr = disposable_redis

    def retry_with_rdb_reload(self):

            yield 1
            self.dr.dump_and_reload()
            yield 2

class DisposableRedis(object):

    def __init__(self, port=None, path='redis-server', **extra_args):
        """
        :param port: port number to start the redis server on. Specify none to automatically generate
        :type port: int|None
        :param extra_args: any extra arguments kwargs will be passed to redis server as --key val
        """

        self._port = port

        # this will hold the actual port the redis is listening on. It's equal to `_port` unless `_port` is None
        # in that case `port` is randomly generated
        self.port = None
        self.extra_args = []
        for k, v in extra_args.items():
            self.extra_args.append('--%s' % k)
            if isinstance(v, (list, tuple)):
                self.extra_args += list(v)
            else:
                self.extra_args.append(v)
             
        
        self.path = path
        self.dumped = False
        self.errored = False


    def _startProcess(self):
        #print("Starting redis process: {}".format(' '.join(self.args)))
        self.process = subprocess.Popen(
            self.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        while True:
            try:
                self.client().ping()
                break
            except redis.ConnectionError:
                self.process.poll()
                if self.process.returncode is not None:
                    raise RuntimeError(
                        "Process has exited with code {}\n. Redis output: {}"
                        .format(self.process.returncode, self.process.stdout.read()))
                
                time.sleep(0.1)

    def __enter__(self):
        if self._port is None:
            self.port = get_random_port()
        else:
            self.port = self._port

        self.dumpfile = 'dump.%s.rdb' % self.port
        self.args = [self.path,
                '--port', str(self.port),
                '--dir', tempfile.gettempdir(),
                '--save', '',
                '--dbfilename', self.dumpfile] + self.extra_args


        self._startProcess()
        return self.client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process.terminate()
        if exc_val or self.errored:
            sys.stderr.write("Redis output: {}\n".format(self.process.stdout.read()))
        if self.dumped:
            try:
                os.unlink(os.path.join(tempfile.gettempdir(), self.dumpfile))
            except OSError:
                pass
            
    def dump_and_reload(self):
        """
        Dump the rdb and reload it, to test for serialization errors
        """

        conn = self.client()
        conn.save()
        self.dumped = True
        try:
            conn.execute_command('DEBUG', 'RELOAD')
        except redis.RedisError as err:
            self.errored = True
            raise err

        

    
  
        
    
    def client(self):
        """
        :rtype: redis.StrictRedis
        """

        return Client(self, self.port)
