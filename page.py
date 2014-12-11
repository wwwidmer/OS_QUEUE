import math
'''
p = 2^k
logical address = l
p# = l/p
offset d = l % p

max proc = m
page/process = m/p
frames = t/p


'''

t = int(raw_input("T: "))
p = int(raw_input("P (2^k): "))
m = int(raw_input("M: "))
l = int(raw_input("l: "))


d = l % p
page = math.ceil(float(l / p))
frames = t / p
pageproc = m/p

print "frames "+str(frames)
print "process/page: "+str(pageproc)
print "offset: "+str(d)
print "page# "+ str(page)

pageTable = []
for x in range(pageproc):
    pageTable.append(x+d)

x = pageTable[int(math.ceil(page))]

print "Frame: "+str(x)

print "Frame + offset: "+ str(x*p + d)
