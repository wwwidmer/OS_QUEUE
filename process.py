from collections import deque
from random import randrange
import re, copy, time, threading


# process object with all essential information. Setters mostly. Nothing complicated.
class pcb(object):

	def __init__(self, pid, memory):
		self.pid = pid
		self.memSize = memory
		self.file = "null"
		self.r = False
		self.lenw = 0
		self.mem = 0
		self.totalTime = 0
		self.cylinder = 1
		self.averageBurst = 0.0
		self.completed = 0

	def updateAverage(self):
		self.averageBurst = float(self.totalTime / self.completed)

	def setFile(self,file):
		self.file = file
	def setR(self, r):
		self.r = r
	def setLenw(self, leng):
		self.lenw = leng
	def setMem(self, mem):
		self.mem = int(mem,16)
	def RW(self):
		return "r" if self.r else "w"
	def __str__(self):
		return str(self.pid)
	def __repr__(self):
		return str(self.pid)+"-"+str(self.memSize)
	def __gt__(self, memR):
		return self.memSize > memR.memSize
	def __lt(self, memR):
		return self.memSize < memR.memSize

# Device object. Uses python deque and can be one of three types. Type really does not matter
# other than printers can only write.
# and Disks have a scheduler
class device(object):
	# printer, disk, CD/RW

	def __init__(self, name):
		self.name = name
		self.queue = deque()
		self.queue_buffer = deque()
		self.averageBurst = 0.0
		self.totalTime = 0
		self.completed = 0
		self.cylinders = 1
		self.cur_cylinder = 1


	def updateTotal(self,x):
		self.completed += 1
		self.totalTime += x


	# DISK SCHEDULER
	def schedule(self):
		dequeuer = []

		try:
			while self.queue_buffer:
				dequeuer.append(self.queue_buffer.popleft())
		except IndexError:
			pass
		dequeuer.reverse()
		while len(dequeuer) >= 1:
			self.curReset()
			if self.cur_cylinder <= self.cylinders:
				boolC = True
				for x in dequeuer:
					if int(x.cylinder) == int(self.cur_cylinder):
						de = dequeuer.pop(dequeuer.index(x))
						self.queue.append(de)
						boolC = False
				if(boolC):
					self.cur_cylinder += 1
			self.curReset()

	def curReset(self):
		if int(self.cur_cylinder) > int(self.cylinders):
			self.cur_cylinder = 1


	def cscanSchedule2(self):
		# thread timer, awake every 4 seconds
		# get cur_cylinder
		# compare to everything in queue_buffer
		# pop from qb into queue is match
		# back to sleep after checking all qb
		pass

	# wrapper methods for the queue
	def popFront(self):
		return self.queue.popleft()
	def push(self,x):
		if self.name[0] == 'd':
			return self.queue_buffer.append(x)
		else:
			return self.queue.append(x)

	# signals the completion of the task in this devices queue
	def terminate(self):
		try:
			return self.queue.popleft()
		except IndexError:
			print "Device is empty"
			return 0

	def checkCylinder(self, x):
		if int(x) > int(self.cylinders):
			return False
		else:
			return True

# cpu object. Where all the fun is.
class cpu(object):

	# create the queue, set the current process to 0 (null), and configure devices attached (as parameter)
	def __init__(self, devices):
		self.queue = deque()
		self.pool = []
		self.runningPCB = 0
		self.devices = []
		self.qSize = 0
		self.avgTime = 0.0
		self.totalTime = 0
		self.numComp = 0
		self.timeSlice = int(devices['slice'])
		self.maxProcessSize = int(devices['maxProc'])
		self.totalMem = int(devices['totalMem'])
		self.currentMemoryAvailable = int(self.totalMem)
		self.pageSize = int(devices['pageSize'])

		for d in range(int(devices['p'])):
			newDevice = device('p'+str(d+1))
			self.devices.append(newDevice)
		for d in range(int(devices['d'])):
			newDevice = device('d'+str(d+1))
			newDevice.cylinders = devices['diskCyl'][d+1]
			self.devices.append(newDevice)
		for d in range(int(devices['rw'])):
			newDevice = device('rw'+str(d+1))
			self.devices.append(newDevice)


	# memory management
	def removeMemory(self,x):
		self.currentMemoryAvailable = self.currentMemoryAvailable - int(x)

	def addMemory(self, x):
		self.currentMemoryAvailable = self.currentMemoryAvailable + int(x)

	def updateAverageCPU(self, x):
		self.numComp += 1
		self.totalTime += x
		self.avgTime = float(self.totalTime / self.numComp)

	def getQueue(self):
		return self.queue
	def getDeviceType(self,device):
		devices = []
		for d in self.devices:
			if d.name[0] == device:
				devices.append(d)
		return devices
	def getDevice(self, device):
		for d in self.devices:
			if d.name == device :
				return d

	# checks device list for a deviceName (p1,d3,rw123132...)
	def findDevice(self,deviceName):
		for d in self.devices:
			if d.name == deviceName:
				return True
		return False

	# We've already popFront at this point, so we set what is currently running to 0
	def terminate(self):
		old = copy.copy(self.runningPCB)
		self.runningPCB = 0
		self.addMemory(old.memSize)
		self.dispatchProcess()
		self.setPCB()
		return old

	# PIDs  must be unique (somewhat) so I'm doing a very simple map/hash
	def pidAssign(self):
		return self.qSize
	# sets the PCB to whatever is at the front of the queue.
	def setPCB(self):
		self.runningPCB = self.popFront()

	def peek(self):
		try:
			return self.queue[0]
		except IndexError:
			print("Nothing in the CPU")
	# fifo data is popped and return. If theres an error we return 0 to indicate there is nothing in the CPU
	def popFront(self):
		try:
			return self.queue.popleft()
		except IndexError:
			print("Nothing in the CPU")
			return 0

	# add to back of the queue
	def push(self,x):
		self.qSize = self.qSize+1
		# check memory left
		# if not enough for X.size add X to pool

		if int(x.memSize) > int(self.currentMemoryAvailable):
			print "To pool"
			self.pool.append(x)
		else:
			self.queue.append(x)
			self.removeMemory(x.memSize)
			if(self.runningPCB == 0):
				self.setPCB()
			return self.runningPCB
			
		
	# determine which process is added to ready queue when memory is freed
	# largest that will fit

	def dispatchProcess(self):
		
		print max(self.pool)
	
	def generatePageTable(self):
		numPages = self.totalMem / self.pageSize
		
		return numPages

	def killProcess(self, pid):
		temp = deque()
		#pop left until found
		if self.runningPCB == 0:
			print "Empty Queue"
			return 0
		elif self.runningPCB.pid == int(pid):
			print "PID#"+str(pid)+" killed."
			self.terminate()
		else:
			while True:
				try:
					x = self.queue.popleft()
					if x.pid == int(pid):
						print "PID#"+str(pid)+" killed."
						self.addMemory(x.memSize)
						break;
					else:
						temp.append(x)
				except IndexError:
					break
			while True:
				try:
					x = temp.pop()
					self.queue.appendleft(x)
				except IndexError:
					break
		self.dispatchProcess()
		return True
