import process
00000
diskCyl = {}
diskCyl[1] = 1

devices = {"slice":1,"totalMem":32,"maxProc":16,"pageSize":4,"p":1,"d":1,"rw":1,"diskCyl":diskCyl}

c = process.cpu(devices)
p0 = process.pcb(1,10)
p1 = process.pcb(2,9)
p2 = process.pcb(3,8)
p3 = process.pcb(4,9)
p5 = process.pcb(5,5)
p6 = process.pcb(6,2)
p7 = process.pcb(8,9)
p4 = process.pcb(7,2)

def info():
    print "Total: " + str(c.totalMem)
    print "Page: " + str(c.pageSize)
    print "Max Process: " + str(c.maxProcessSize)
    print "Current memory: " + str(c.currentMemoryAvailable)
    print "---------------"
    print "Frame Table Size: " + str(c.totalMem/c.pageSize)
    print "Page Table Size: " + str(c.maxProcessSize/c.pageSize)


c.push(p0)
c.push(p1)
c.push(p2)
c.push(p3)
c.push(p4)
c.push(p5)
info()

print c.pool


print c.runningPCB
print "."
for x in c.queue:
    print x.pid

print "======"
print c.pool
c.killProcess(1)
info()
c.killProcess(2)
print c.runningPCB
print "."
for x in c.queue:
    print x.pid
print "======"

print c.pool
info()
print c.runningPCB
print "."
for x in c.queue:
    print x.pid
print "======"



