from collections import deque
from random import randrange

# process object with all essential information. Setters mostly. Nothing complicated.
class pcb(object):

	def __init__(self, pid):
		self.pid = pid
		self.r = False
		self.lenw = 0
		self.mem = 0
	def setR(self, r):
		self.r = r
	def setLenw(self, len):
		self.lenw = len
	def setMem(self, mem):
		self.mem = mem

# Device object. Usese python deque and can be one of three types. Type really does not matter 
# other than printers can only write.
class device(object):
	# printer, disk, CD/RW 
	# read / write

	def __init__(self, name):
		self.name = name
		self.queue = deque()

	# wrapper methods for the queue
	def popFront(self):
		return self.queue.popleft()
	def push(self,x):
		return self.queue.append(x)
	# communicates with cpu somehow but perhaps I won't even need this
	def sendInterupt():
		pass


# cpu object. Where all the fun is.
class cpu(object):

	# create the queue, set the current process to 0 (null), and configure devices attached (as parameter)
	def __init__(self, numDevices):
		self.queue = deque()
		self.runningPCB = 0
		self.devices = []
		for d in numDevices:
			for i in range(int(numDevices[d])):
				newDevice = device(d+str(i+1))
				self.devices.append(newDevice)
		
	# checks device list for a deviceName (p1,d3,rw123132...)
	def findDevice(self,deviceName):
		for d in self.devices:
			if d.name == deviceName:
				return True
		return False

	# We've already popFront at this point, so we set what is currently running to 0
	def terminate(self):
		self.runningPCB = 0
		self.setPCB()

	# PIDs must be unique (somewhat) so I'm doing a very simple map/hash 
	def pidAssign(self):
		return randrange(self.qSize()+1) % 32
	# sets the PCB to whatever is at the front of the queue. 
	def setPCB(self):
			self.runningPCB = self.popFront()
	def qSize(self):
		return len(self.queue)
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
		self.queue.append(x)
		if(self.runningPCB == 0):
			self.setPCB()
		return self.runningPCB

