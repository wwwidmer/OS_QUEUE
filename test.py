import process


d = process.device("d1")
d.cylinders = 8

p1 = process.pcb(0)
p1.cylinder = 1
p3 = process.pcb(2)
p3.cylinder = 7

d.push(p1) #1
d.schedule()
d.push(p1) #1
d.push(p3) #7
d.schedule()
d.push(p1) #1
d.push(p3) #7
d.schedule()
d.push(p3) #7
d.push(p1) #1
d.push(p3) #7
d.push(p3) #7
d.push(p1) #1
d.push(p3) #7
d.push(p1) #1
d.schedule()

# 1 1 7 7 1 1 1 1 7 7 7 7


for x in d.queue:
	print x.cylinder
