from collections import deque
from random import randrange
import re, copy

# process object with all essential information. Setters mostly. Nothing complicated.
class pcb(object):

	def __init__(self, pid):
		self.pid = pid
		self.file = "null"
		self.r = False
		self.lenw = 0
		self.mem = 0
		self.totalTime = 0
		self.cylinder = 0

	def setFile(self,file):
		self.file = file
	def setR(self, r):
		self.r = r
	def setLenw(self, len):
		self.lenw = len
	def setMem(self, mem):
		self.mem = mem
	def RW(self):
		return "r" if self.r else "w"

# Device object. Usese python deque and can be one of three types. Type really does not matter
# other than printers can only write.
class device(object):
	# printer, disk, CD/RW

	def __init__(self, name):
		self.name = name
		self.queue = deque()
		self.averageBurst = 0
		self.totalTime = 0
		self.completed = 0
		self.cylinders = 0

	def updateAverage(self):
		self.averageBurst = (self.totalTime / self.completed)

	def updateTotal(self,x):
		self.completed += 1
		self.totalTime += x

	def schedule(self):
		# if disk queue do sched
		pass

	def cscanSchedule(self):
		pass
	# wrapper methods for the queue
	def popFront(self):
		return self.queue.popleft()
	def push(self,x):
		return self.queue.append(x)
	# signals the completion of the task in this devices queue
	def terminate(self):
		try:
			return self.queue.popleft()
		except IndexError:
			print "Device is empty"
			return 0
	def checkCylinder(self, x):
		if int(x) > self.cylinders:
			return False
		else:
			return True

# cpu object. Where all the fun is.
class cpu(object):

	# create the queue, set the current process to 0 (null), and configure devices attached (as parameter)
	def __init__(self, devices):
		self.queue = deque()
		self.runningPCB = 0
		self.devices = []
		self.qSize = 0
		self.avgTime = 0
		self.timeSlice = int(devices['slice'])
		# 	return {"p":numprint,"d":numdisk,"rw":numrw,"slice":tSlice,"diskCyl":diskCyl}
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
		self.setPCB()
		return old

	# PIDs must be unique (somewhat) so I'm doing a very simple map/hash
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
		self.queue.append(x)
		if(self.runningPCB == 0):
			self.setPCB()
		return self.runningPCB

	# round robin, if cur time slice is taken up, place process into back of queue
	def schedule(self):
		pass
