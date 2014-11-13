import process


d = process.device("d1")
d.cylinders = 4

p1 = process.pcb(1)
p1.cylinder = 2
p2 = process.pcb(5)
p2.cylinder = 3

d.push(p1)
d.push(p1)
d.push(p2)
d.push(p1)
d.push(p1)
d.push(p2)

d.schedule()

for x in d.queue:
	print x.cylinder
