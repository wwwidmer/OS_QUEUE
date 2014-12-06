from process import pcb, device, cpu
import re, copy


# GENERATE SYSTEM PARAMETERS FROM INPUT
# TRAPS ALL INCORRECT TYPES
def sysgen():
	print("SYSGEN")
	deviceGen = False
	while(not deviceGen):
		numprint=raw_input("How many printers are connected to the system?: ")
		numdisk=raw_input("How many disks are connected to the system?: ")
		numrw=raw_input("How many CD/RW are connected to the system?: ")
		tSlice = raw_input("How long is a time slice?: ")
		totalMem = raw_input("What is the total size of memory?(All memory sizes are in words): ")
		maxProc = raw_input("What is the maximum size of a process?: ")
		pageSize = raw_input("What is the sixe of a page?: ")		
				
		deviceGen = genIntCheck([numprint, numdisk, numrw, tSlice,totalMem,maxProc,pageSize])

		if deviceGen:
			if not power2(int(pageSize)) or int(totalMem) % int(pageSize) != 0:
				print "Page size must be a power of 2 and must evenly divide Total Memory"			
				deviceGen = False
		
		# check mem,proc,pagesize for correct sizes
		# page size is a power of 2
		# page should divide all memory evenly
				
		if(not deviceGen):
			print "Please reenter all values as base 10 Integers"
		# determine cylinder length for each disk
	diskCyl = {}
	generatingDisk = True
	while generatingDisk:
		for i in range(int(numdisk)):
			cyl = raw_input("How many cylinders does the "+str(i+1)+"th disk have?: ")
			diskCyl[i+1] = cyl
		if genIntCheck(diskCyl.values()):
			generatingDisk = False
		else:
			generatingDisk = True
			print("Please reenter all values as base 10 Integers")


	return {"p":numprint,"d":numdisk,"rw":numrw,"slice":tSlice,"diskCyl":diskCyl,"totalMem":totalMem,"maxProc":maxProc,"pageSize":pageSize}

# check for power of 2 oneliner
def power2(x):
	return (x & (x-1) == 0) and (x != 0)


def hexCheck(x):
	try:
		int(x,16)
		return True
	except TypeError:
		return False
	except ValueError:
		return False

# a type checker for sysgen
def genIntCheck(a):
		try:
			for i in a:
				int(i)
		except TypeError:
			return False
		except ValueError:
			return False
		return True


# a loop to prompt the user for the next command.
def running(cpu):
	running = True
	print("Running")
	while(running):
		command = raw_input("Enter a command: ")
		handleInput(command,cpu)

# check for regular expression of commands that can be variable (p1, w1, etc)
# or commands mapped to functions that are essentially static (t, A, S)
def handleInput(command,cpu):
	known_commands = {"A":processArrival, "S":snapshot, "t":terminate, "T":backtoQueue}
	regCommands = re.match(r'^(?P<device>p|d|rw)(?P<number>[0-9]+)$', command)
	termCommands = re.match(r'^(?P<device>P|D|RW)(?P<number>[0-9]+)$', command)
	killCommand = re.match(r'^K(?P<number>[0-9]+)$',command)
	if(regCommands):
		regCommands.groupdict()
		currentPCB = copy.copy(cpu.runningPCB)
		# check we have a running process
		try:
			currentPCB.pid
		except AttributeError:
			print "No process in CPU"
			return 0
		# check if device exists
		if(not cpu.findDevice(command.lower())):
			print "Device not found"
			return 0
		else:
			paraFile = raw_input("Enter filename: ")
			currentPCB.setFile(paraFile)
			setRead = 'w'
			if not command.lower()[0] == 'p':
				setRead = raw_input("Read or Write: ")
				if setRead == 'r':
					currentPCB.setR == True
				elif setRead =='w':
					currentPCB.setR == False
				else:
					print "Unknown command\n"
					return 0
			paraMem = raw_input("Enter memory starting location(hex): ")
			if(hexCheck(paraMem)):
				currentPCB.setMem(paraMem)
				# CORRESPONDING PHYSICAL ADDRESS
			else:
				print "Please use base 16 integer"
				return 0
			if(setRead == 'w'):
				para2 = raw_input("Memory length(int): ")
				if genIntCheck([para2]):
					currentPCB.setLenw(para2)
				else:
					print "Incorrect, please use base 10 integer"
					return  0
			if(command.lower()[0] == 'd'):
				cylinderAccess = raw_input("Which cylinder?: ")
				try:
					int(cylinderAccess)
					if(cpu.getDevice(command.lower()).checkCylinder(cylinderAccess)):
						currentPCB.cylinder = cylinderAccess
					else:
						print "Cylinder does not exist in this disk."
						return 0
				except ValueError:
					print "Please enter an integer."
					return 0
			# prompt Timer Here
			timerInt = False
			timerPrompt = 0
			while not timerInt:
				timerPrompt = raw_input("How long was this process in the CPU before syscall?: ")
				timerInt = genIntCheck([timerPrompt])
				if not timerInt:
					print "Incorrect, please use base 10 integer"
				elif int(timerPrompt) > cpu.timeSlice:
					print "Timer is larger than a time slice, try again"
					timerInt = False
				elif int(timerPrompt) < 0:
					print "Timer should be non-negative base 10 integer"
					timerInt = False

			currentPCB.totalTime += int(timerPrompt)
			currentPCB.completed += 1
			currentPCB.updateAverage()
			cpu.getDevice(command.lower()).push(currentPCB)
			cpu.setPCB()
	elif (termCommands):
		processBackToCpu = cpu.getDevice(command.lower()).terminate()
		if(processBackToCpu == 0):
			print "There was an error and it was not handled"
			print "From my tests this means a process was sent to Disk"
			print "But was not scheduled"
		else:
			cpu.push(processBackToCpu)
	elif (killCommand):
		kill(cpu,command[1:])
	else:
		try:
			if(known_commands[command]):
				known_commands[command](cpu)
		except KeyError as k:
			print "Unknown Command. Try again"
#K#

def kill(cpu,pid):
	old = cpu.killProcess(pid)
	if old == 0:
		print "PID could not be found"
		return 0
	print "{:4s} {:10s}".format("PID","Total CPU Time")
	print "{:4s} {:10s}".format(str(old.pid),str(old.totalTime))
	
	cpu.updateAverageCPU(old.totalTime)
	print cpu.avgTime

# 'T'
def backtoQueue(cpu):
	currentPCB = copy.copy(cpu.runningPCB)
	if currentPCB == 0:
		print "Nothing in CPU"
		return 0
	else:
		currentPCB.totalTime += cpu.timeSlice
		cpu.addMemory(currentPCB.memSize)
		cpu.setPCB()
		cpu.push(currentPCB)

# 'A'
def processArrival(cpu):
	pid = cpu.pidAssign()
	wordCheck = False
	while(not wordCheck):
		words = raw_input("Size of process (words): ")
		wordCheck = genIntCheck([words])
		
		if not wordCheck:
			print "Please enter a base-10 integer less than the maximum size of a process and maximum size of memory."
		if wordCheck:
			if int(words) > cpu.totalMem or int(words) > cpu.maxProcessSize or int(words) == 0:
				print "Please let process be smaller than the CPUs total memory and the max process size"
				wordCheck = False

	process = pcb(pid,words)
	cpu.push(process)

# 't'
def terminate(cpu):
	old = cpu.terminate()
	if old == 0:
		print "There was nothing in the CPU"
		return 0
	# calculate average time
	print "{:4s} {:10s}".format("PID", "Total CPU Time")
	print "{:4s} {:10s}".format(str(old.pid), str(old.totalTime))
	cpu.updateAverageCPU(old.totalTime)
	print cpu.avgTime

# 'S'
def snapshot(cpu):
	sPara = raw_input("Enter r, p, d, c, or m: ")
	print "Average CPU time"
	print cpu.avgTime
	if sPara == 'r':
		print 'Ready Queue (First is currently in CPU)\n'
		snapshotReadyQueue(cpu, cpu.getQueue() )
	elif sPara == 'p':
		snapshotOutput( cpu.getDeviceType("p") )
	elif sPara == 'd':
		snapshotOutput( cpu.getDeviceType("d") )
	elif sPara == 'c':
		snapshotOutput( cpu.getDeviceType("r") )
	elif sPara == 'm':
		snapshotMemory()
	else:
		print "Unknown Command\n"

# S m
def snapshotMemory(cpu):
	pass


# S r
def snapshotReadyQueue(cpu,queue):
	print '{:4s} \n'.format('PID')
	if cpu.runningPCB == 0:
		print "Nothing in CPU"
	else:
		print cpu.runningPCB.pid
	for pcb in queue:
		print '{:4s} '.format(str(pcb.pid))

# S everything else
def snapshotOutput(device):
	print '{:4s} {:15s} {:10s} {:5s} {:8s} {:7s} {:5s} {:7s}\n'.format('PID','Filename','Memstart','R/W','File','Length','Time', 'AvgBurst')
	for d in device:
		if d.name[0] == 'd':
			d.schedule()
		print '--- {:3s}\n'.format(d.name)
		for pcb in d.queue:
			print '{:4s} {:15s} {:10s} {:5s} {:8s} {:7s} {:5s} {:7s}\n'.format(str(pcb.pid), pcb.file, str(hex(pcb.mem)), pcb.RW(), str(pcb.mem), str(pcb.lenw), str(pcb.totalTime), str(pcb.averageBurst))

# Call appropriate functions, generate system, link CPU and devices, run with the one CPU.
def init():
	devices = sysgen()
	mainCPU = cpu(devices)
	running(mainCPU)

if __name__ == "__main__":
	init()
