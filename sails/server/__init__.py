import threading
import time

from sails.server.control.pykernel import ipy_kernel


class Server(object):

    def __init__(self):
        self.kernel_thread = threading.Thread(target=ipy_kernel, args=(self,))
        self.kernel_thread.run()

    def start_loop(self):
        while True:
            time.sleep(1)
