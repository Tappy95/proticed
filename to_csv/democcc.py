from multiprocessing import Process, Queue
import os
from time import sleep


class tt:
    def __init__(self, q):
        self.a_lis = q

    def work_project(self, i):
        print(i)
        sleep(3)
        self.a_lis.put(i)

    def main(self):
        process_list = []
        # process_list = multiprocessing.Manager().list()
        for i in range(3):
            process = Process(target=self.work_project, args=(i, ))
            process.start()
            process_list.append(process)
        for p in process_list:
            p.join()
        print([self.a_lis.get() for k in range(self.a_lis.qsize())])


if __name__ == '__main__':
    q = Queue()
    tt(q).main()
