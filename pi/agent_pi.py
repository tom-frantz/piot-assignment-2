"""
Driver class for Agent Pi
"""

from agent.cli.menu import Menu,Things
from agent.sockets.operation import *
import threading
import queue
import time

send_queue = queue.Queue()
recv_queue = queue.Queue()


def start():
    """
    Two threads operation:

    1. Menu thread
    2. Socket client thread
    """

    t1 = threading.Thread(target=Menu().run, args=(send_queue, recv_queue))
    t2 = threading.Thread(target=client_start, args=(send_queue, recv_queue))
    t3 = threading.Thread(target=Things().search_bluetooth, args=(send_queue, recv_queue))
    print("Systm is scanning engineers' devices, please wait.")
    a = t3.start()
    t2.start()
    time.sleep(30)
    t1.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    start()
