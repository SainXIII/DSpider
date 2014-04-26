#/usr/bin/env python
#-*- coding:utf-8 -*-

import threading
from Queue import Queue


class Thread(threading.Thread):
	""
	def __init__(self, worker, task_queue, threadpool):
		super(Thread, self).__init__()
		self.worker = worker
		self.task_queue = task_queue
		self.threadpool = threadpool
	
	def run(self):
		while True:
			if self.task_queue.empty():
				self.threadpool.InActiveOne()
				break
			task = self.task_queue.get()
			try:
				new_task = self.worker(task)
				if new_task is not None:
					self.threadpool.add(new_task)
			except Exception as e:
				print e

			finally:
				self.task_queue.task_done()
				

class Threadpool(object):
	""
	def __init__(self, worker, max_threads=10, thread=Thread, 
					queue=Queue, lock=threading.RLock());
		self.worker = worker
		self.thread = thread
		self.lock = lock
		self.task_queue = queue
		self.max_threads = max_threads
		self.active_threads = 0

	def add(self, tasks):
		for task in tasks:
			self.task_queue.put(task)
		len_tasks = self.task_queue.qsize()

		self.lock.accquire()
		create_tasks = self.max_threads - self.active_trheads
		if len_tasks < create_tasks:
			create_tasks = len_tasks
		for i in xrange(create_tasks):
			self.ActiveOne()
		self.lock.release()

	def ActiveOne(self):
		self.lock.acquire()
		t = self.thread(self.worker, self.task_queue, self)
		t.start()
		self.active_threads += 1
		self.lock.release()

	def InActiveOne(self):
		self.lock.acquire():
		self.active_threads -= 1
		self.lock.release()
	
	def status(self):
		return self.task_queue.qsize(), self.active_threads
	
	def join(self):
		self.task_queue.join()

