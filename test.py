import process

diskCyl = {}
diskCyl[1] = 1

devices = {"slice":1,"totalMem":40,"maxProc":10,"pageSize":4,"p":1,"d":1,"rw":1,"diskCyl":diskCyl}

c = process.cpu(devices)
p0 = process.pcb(1,10)
p1 = process.pcb(2,10)
p2 = process.pcb(3,2)
p3 = process.pcb(4,10)
p5 = process.pcb(5,4)
p6 = process.pcb(6,9)
p7 = process.pcb(8,8)
p4 = process.pcb(7,6)

def info():
    print "total memory: " + str(c.totalMem)
    print "page size: " + str(c.pageSize)
    print "current memory: " + str(c.currentMemoryAvailable)



c.push(p0)
c.push(p1)
c.push(p2)
c.push(p3)
c.push(p4)
c.push(p5)
c.push(p6)
c.push(p7)
info()

print c.pool

for x in c.queue:
    print x.pid

print "======"
c.killProcess(4)


for x in c.queue:
    print x.pid
print "======"

c.killProcess(1)
info()



