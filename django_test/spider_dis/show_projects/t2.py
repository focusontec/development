import Queue
import threading
import time

class WorkerManager(object):
    def __init__(self,work_num,tread_num):
        self.work_queue = Queue.Queue()
        self.thread = []
        self.__init_work_queue(work_num)
        self.__init_thread_pool_num(tread_num)

    def __init_thread_pool_num(self, tread_num):
        for i in range(tread_num):
            self.thread.append(Work(self.work_queue))

    def __init_work_queue(self, job_num):
        for i in range(job_num):
            self.add_job(do_job,i)

    def add_job(self,func,*args):
        self.work_queue.put((func,list(args)))

    def wait_allcomplete(self):
        for item in self.thread:
            if item.isAlive():item.join()


class Work(threading.Thread):
    def __init__(self,work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()
    def run(self):
        while True:
            try:
                do,args = self.work_queue.get(block = False)
                do(args)
            except:
                break
def do_job(args):

    print threading.current_thread().list(args)
    time.sleep(1)

if __name__ == '__main__':
    start_time = time.time()
    work_manager = WorkerManager(10000,10)
    work_manager.wait_allcomplete()
    end_time = time.time()
    print 'cost all time :{}'.format(end_time-start_time)









