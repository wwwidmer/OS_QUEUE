from process import pcb, device, cpu
import re, copy


# GENERATE SYSTEM PARAMETERS FROM INPUT
# Trap all incorrect types (String instead of numbers)
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
                # Validate all input as integers.
                deviceGen = genIntCheck([numprint, numdisk, numrw, tSlice,totalMem,maxProc,pageSize])
                # Validate Page size to be a power of 2
		if deviceGen:
			if not power2(int(pageSize)) or int(totalMem) % int(pageSize) != 0:
				print "Page size must be a power of 2 and must evenly divide Total Memory"			
				deviceGen = False
                # If we weren't given Integers
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

        # Map the user input and return.
	return {"p":numprint,"d":numdisk,"rw":numrw,"slice":tSlice,"diskCyl":diskCyl,"totalMem":totalMem,"maxProc":maxProc,"pageSize":pageSize}

# Check for power of 2 oneliner
def power2(x):
	return (x & (x-1) == 0) and (x != 0)


# Check for hex
def hexCheck(x):
	try:
		int(x,16)
		return True
	except TypeError:
		return False
	except ValueError:
		return False

# Check all members of [a] as integer. Useful for sysgen.
def genIntCheck(a):
		try:
			for i in a:
				int(i)
		except TypeError:
			return False
		except ValueError:
			return False
		return True


# An endless loop to prompt the user for the next command.
def running(cpu):
	running = True
	print("Running")
	while(running):
		command = raw_input("Enter a command: ")
		handleInput(command,cpu)

# Check for regular expression of commands that can be variable (p1, w1, etc)
# Or commands mapped to functions that are essentially static (t, A, S)
def handleInput(command,cpu):
        # Map of known commands vs regex of other potential commands.
        known_commands = {"A":processArrival, "S":snapshot, "t":terminate, "T":backtoQueue}
	regCommands = re.match(r'^(?P<device>p|d|rw)(?P<number>[0-9]+)$', command)
	termCommands = re.match(r'^(?P<device>P|D|RW)(?P<number>[0-9]+)$', command)
	killCommand = re.match(r'^K(?P<number>[0-9]+)$',command)
        # If we have a regular command
	if(regCommands):
		regCommands.groupdict()
		currentPCB = copy.copy(cpu.runningPCB)
		# Check we have a running process
		try:
			currentPCB.pid
		except AttributeError:
			print "No process in CPU"
			return 0
		# Check if device exists
		if(not cpu.findDevice(command.lower())):
			print "Device not found"
			return 0
		else:
                        # Get all required parameters for the current pcb.
                        paraFile = raw_input("Enter filename: ")
			currentPCB.setFile(paraFile)
			setRead = 'w'
                        # Printers can only write.
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
				if int(paraMem,16) > cpu.maxProcessSize:
					print "Input larger than Logical Memory"
					return 0
				print "Physical Address: " + str(currentPCB.setMem(paraMem))
			else:
				print "Please use base 16 integer"
				return 0
                        # If we're writing we need a memory length.
			if(setRead == 'w'):
				para2 = raw_input("Memory length(int): ")
				if genIntCheck([para2]):
					currentPCB.setLenw(para2)
				else:
					print "Incorrect, please use base 10 integer"
					return  0
                        # If we're using a disk define which cylinder used.
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
			# Prompt Timer Here. Every process in the ready queue must be timed.
			timerInt = False
			timerPrompt = 0
			while not timerInt:
				timerPrompt = raw_input("How long was this process in the CPU before syscall?: ")
				timerInt = genIntCheck([timerPrompt])
				if not timerInt:
					print "Incorrect, please use base 10 integer"
                                # At this point we can just call int() because this part of the code is not reached
                                # Because incorrect input is trapped.
				elif int(timerPrompt) > cpu.timeSlice:
					print "Timer is larger than a time slice, try again"
					timerInt = False
				elif int(timerPrompt) < 0:
					print "Timer should be non-negative base 10 integer"
					timerInt = False
                        # Update averages, push PCB to correct device, determine new head of the queue.
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
# K#. End a process. 
def kill(cpu,pid):
	old = cpu.kill(pid)
	if old == 0:
		print "PID could not be found"
		return 0
	print "{:4s} {:10s}".format("PID","Total CPU Time")
	print "{:4s} {:10s}".format(str(old.pid),str(old.totalTime))
	cpu.dispatchProcess()
	cpu.updateAverageCPU(old.totalTime)
	print "Average CPU time"
	print cpu.avgTime

# 'T', Pop and push a process back onto the ready queue. Tau = a whole time slice.
def backtoQueue(cpu):
	currentPCB = copy.copy(cpu.runningPCB)
	if currentPCB == 0:
		print "Nothing in CPU"
		return 0
	else:
		currentPCB.totalTime += cpu.timeSlice
		cpu.setPCB()
		cpu.push(currentPCB)

# 'A', a new Process
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

	process = pcb(pid,words,cpu.maxProcessSize,cpu.pageSize)
	# Check if we have enough pages. If not add to job pool.
	# If we do we can get frames and generate table
	# Then push into the cpu
	if process.tableSize() > len(cpu.frames):
		print "This process has been added to the pool"
		cpu.pool.append(process)
	else:
		frames = cpu.removeMemory(process.tableSize())
		process.generateTable(frames)
		cpu.push(process)

# 't', kills the current process.
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

# 'S' - Entire section is Output from the S command.
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
		snapshotMemory(cpu)
	else:
		print "Unknown Command\n"

# S m
def snapshotMemory(cpu):
	cpu.memorySnapshot()


# S r
def snapshotReadyQueue(cpu,queue):
	print '{:4s}'.format('PID')
	if cpu.runningPCB == 0:
		print "Nothing in CPU"
	else:
		print '{:4s}'.format(str(cpu.runningPCB.pid)) + "Frames: " + str(cpu.runningPCB.table)
	for pcb in queue:
		print '{:4s} '.format(str(pcb.pid)) +"Frames: "+ str(pcb.table)


# S everything else
def snapshotOutput(device):
	print '{:4s} {:10s} {:5s} {:5s} {:8s} {:7s} {:5s} {:7s} {:10s}\n'.format('PID','Filename','Mem0x','R/W','File','Length','Time', 'AvgBurst', 'Frames')
	for d in device:
		if d.name[0] == 'd':
			d.schedule()
		print '--- {:3s}\n'.format(d.name)
		for pcb in d.queue:
			print '{:4s} {:10s} {:5s} {:5s} {:8s} {:7s} {:5s} {:7s} {:10s}\n'.format(str(pcb.pid), pcb.file, str(hex(pcb.mem)), pcb.RW(), str(pcb.mem), str(pcb.lenw), str(pcb.totalTime), str(pcb.averageBurst), str(pcb.table))

# Call appropriate functions, generate system, link CPU and devices, run with the one CPU.
def init():
	devices = sysgen()
	mainCPU = cpu(devices)
	running(mainCPU)

if __name__ == "__main__":
	init()
