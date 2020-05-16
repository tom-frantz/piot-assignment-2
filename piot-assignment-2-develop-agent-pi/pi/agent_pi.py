from agent.cli.menu import Menu
from agent.sockets.operation import *
import threading,queue
import time

send_queue = queue.Queue()
recv_queue = queue.Queue()

def start():
    t1 = threading.Thread(target=Menu().run, args=(send_queue,recv_queue))
    t2 = threading.Thread(target=client_start, args=(send_queue,recv_queue))
    t2.start()
    time.sleep(2)
    t1.start()
    t1.join()
    t2.join()

if __name__ == '__main__':
    start()