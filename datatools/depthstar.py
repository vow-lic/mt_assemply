with open('logdepth','r') as fin:
    c = []
    for line in fin:
        inf = line.strip().split()
        c.append(int(inf[2]))
m = max(c)
for i in range(m+1):
    print i,c.count(i)
