from process import pcb, device, cpu
import re


# system generation function.
def sysgen():
	print("SYSGEN")
	deviceGen = True
	while(deviceGen):
		numprint=raw_input("How many printers are connected to the system?\n")
		numdisk=raw_input("How many disks are connected to the system?\n")
		numrw=raw_input("How many CD/RW are connected to the system?\n")
		deviceGen = genIntCheck([numprint, numdisk, numrw])
		if(deviceGen):
			print "Please reenter all values as base 10 Integers"

	print("System Generating with %s printers, %s disks, and %s CD/RW" % (numprint, numdisk, numrw))
	return {"p":numprint,"d":numdisk,"rw":numrw}

# a type checker for sysgen
def genIntCheck(a):
		try:
			for i in a:
				int(i)
		except TypeError:
			return True
		except ValueError:
			return True
		return False


# a loop to prompt the user for the next command.
def running(cpu):
	running = True
	print("Running")
	while(running):
		command = raw_input("Enter a command:\n")
		handleInput(command,cpu)

# check for regular expression of commands that can be variable (p1, w1, etc)
# or commands mapped to functions that are essentially static (t, A, S)
def handleInput(command,cpu):
	known_commands = {"A":processArrival, "S":snapshot, "KILLALL":exit, "exit":exit, "t":terminate}
	regCommands = re.match(r'^(?P<device>p|d|rw|P|D|RW)(?P<number>[0-9]+)$', command)
	if(regCommands):
		regCommands.groupdict()
		currentPCB = cpu.runningPCB
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
			paraCommand = raw_input("Enter filename, r, w, or memory: ")
			if not genIntCheck([paraCommand]):
				currentPCB.setMem(paraCommand)
				para2 = raw_input("Memorys length: ")
				if not genIntCheck([para2]):
					currentPCB.setLenw(para2)
				else:
					print "Incorrect, please use base 10 integer"
			elif paraCommand == 'w':
				currentPCB.setR(False)
			elif paraCommand == 'r':
				currentPCB.setR(True)
			else:
				currentPCB.setFile(paraCommand)
			cpu.getDevice(command.lower()).push(currentPCB)
		# handle more input (check for P D RW vs p d rw)
		# memory (int) , 'r', 'w', how long 'w' is. Printer only takes 'w'

	else:
		try:
			if(known_commands[command]):
				known_commands[command](cpu)
		except KeyError as k:
			print "Unknown Command. Try again"


# 'A'
def processArrival(cpu):
	pid = cpu.pidAssign()
	process = pcb(pid)
	cpu.push(process)

# 't'
def terminate(cpu):
	cpu.terminate()

# 'S'
def snapshot(cpu):
	sPara = raw_input("Enter r, p, d, or c\n")

	if sPara == 'r':
		print "r"
	elif sPara == 'p':
		snapshotOutput( cpu.getDeviceType("p") )
	elif sPara == 'd':
		print "d"
	elif sPara == 'c':
		print "c"
	else:
		print "Unknown Command"

	#r
	# show the PIDs of the proceses in the REady Q
	#p
	# show the PIDs and printer information of the processes in the printer queues
	#d
	# above for disks
	#c
	# CD/RW queues

def snapshotOutput(device):

		print '{:4s} {:20s} {:10s} {:5s} {:8s} {:7s}\n'.format('PID','Filename','Memstart','R/W','File','Length')
		for d in device:
			print '--- {:3s}\n'.format(d.name)
			for pcb in d.queue:
				print '{:4s} {:20s} {:10s} {:5s} {:8s} {:7s}\n'.format(str(pcb.pid), pcb.file, str(pcb.mem), pcb.RW(), pcb.file, str(pcb.lenw))




# Call appropriate functions, generate system, link CPU and devices, run with the one CPU.
def init():
	devices = sysgen()
	mainCPU = cpu(devices)
	running(mainCPU)


if __name__ == "__main__":
	init()
