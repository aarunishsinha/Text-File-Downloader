import socket
import hashlib
import threading
import heapq
import time
import sys
import pandas as pd
import numpy as np

byte = 0
class PriorityQueue:
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
downloaded_chunks = PriorityQueue()
def chunk_alloc(size):
    global byte
    if (byte + size) >= 6488666:
        byte_range = str(byte)+'-'+str(6488666)
        byte = 6488666
        return byte_range
    byte_range = str(byte)+'-'+str(byte+size)
    # print (byte_range)
    byte += size
    byte += 1
    return byte_range
def make_requests(size, host, lock):
    global byte
    global downloaded_chunks
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysock.settimeout(15)
    mysock.connect((host, 80))
    while not byte == 6488666:
        # print (byte)
        lock.acquire()
        byte_range = chunk_alloc(size)
        lock.release()
        cmd = "GET /big.txt HTTP/1.1\r\nHost: %s\r\nConnection: keep-alive\r\nRange: bytes=%s\r\n\r\n" % (host, byte_range)
        mysock.send(cmd.encode())
        flag = False
        check_header = ""
        data_str = ""
        while True:
            if not flag:
                try:
                    data = mysock.recv(1)
                except:
                    mysock.close()
                    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    mysock.settimeout(15)
                    # mysock.settimeout(1000)
                    while True:
                        try:
                            mysock.connect((host, 80))
                            # mysock.connect((host, 80))
                        except:
                            mysock.close()
                            mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            mysock.settimeout(15)
                        else:
                            mysock.send(cmd.encode())
                            check_header = ""
                            break
                    continue
                else:
                    if len(data) < 1:
                        check_header = ""
                        continue
                    check_header = check_header + data.decode()
                finally:
                    if '\r\n\r\n' in check_header:
                	       flag = True
            else:
                i = 0
                while i < (size+1):
                    try:
                        data = mysock.recv(1)
                    except:
                        mysock.close()
                        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        mysock.settimeout(15)
                        # mysock.settimeout(1000)
                        while True:
                            try:
                                mysock.connect((host, 80))
                                # mysock.connect((host, 80))
                            except:
                                mysock.close()
                                mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                mysock.settimeout(15)
                            else:
                                mysock.send(cmd.encode())
                                data_str = ""
                                check_header = ""
                                flag = False
                                break
                        break
                    else:
                        data_str += (data.decode() + '')
                        i += 1
                if flag:
                    break
        downloaded_chunks.update(data_str, int(byte_range.split('-')[0]))
        # print ("Range Downloaded:",byte_range)
    mysock.close()
def store_in_file(filename):
    global downloaded_chunks
    f = open(filename, 'w')
    while not downloaded_chunks.isEmpty():
        chunk = downloaded_chunks.pop()
        # print (chunk)
        f.write(chunk)
    f.close()

if __name__ == '__main__':
    start_time = time.time()
    lock = threading.Lock()
    threads = []
    host = sys.argv[1]
    num_threads = sys.argv[2]
    source = host.split('.')[1]
    filename = source + '_big.txt'
    for i in range(int(num_threads)):
        t = threading.Thread(target=make_requests, args=(102399, host, lock, ))
        threads.append(t)
    # for i in range(int(num_threads/2)):
    #     t = threading.Thread(target=make_requests, args=(102399, 'www.norvig.com', lock, ))
    #     threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end_time = time.time()
    store_in_file(filename)
    md5 = hashlib.md5((open(filename, 'r')).read().encode()).hexdigest()
    print ('MD5 Sum:',md5)
    print ('Time taken:', (end_time-start_time))
