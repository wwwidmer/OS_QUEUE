import process

diskCyl = {}
diskCyl[1] = 1

devices = {"slice":1,"totalMem":3072,"maxProc":1024,"pageSize":256,"p":1,"d":1,"rw":1,"diskCyl":diskCyl}

c = process.cpu(devices)
p0 = process.pcb(1,1000, 1024, 256)
p1 = process.pcb(2,900, 1024, 256)
p2 = process.pcb(3,800, 1024, 256)
p3 = process.pcb(4,600, 1024, 256)
p4 = process.pcb(8,500, 1024, 256)
p5 = process.pcb(8,500, 1024, 256)

def info():
    print "Total: " + str(c.totalMem)
    print "Page: " + str(c.pageSize)
    print "Max Process: " + str(c.maxProcessSize)
    print "Current memory: " + str(c.frames)
    print "---------------"
    print "Frame Table Size: " + str(c.totalMem/c.pageSize)
    print "Page Table Size: " + str(c.maxProcessSize/c.pageSize)


p4.generateTable(c.removeMemory(p4.tableSize()))
p1.generateTable(c.removeMemory(p1.tableSize()))
p2.generateTable(c.removeMemory(p2.tableSize()))
p3.generateTable(c.removeMemory(p3.tableSize()))


c.push(p4)
c.push(p1)
c.push(p2)
#c.push(p3)
'''
c.push(p1)
c.push(p2)
c.push(p3)
c.push(p4)
c.push(p5)
'''
info()

l = 258

print "table " + str(p4.table)
print "table " + str(p1.table)
print "table " + str(p2.table)


print p4.getPhysicalPage(l)

c.addMemory(p4)
print c.frames

c.memorySnapshot()




'''
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
'''



