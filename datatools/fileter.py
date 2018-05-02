with open('s300_5x_kmercount.txt','r') as fin:
    with open('5x_50.txt','w') as fout:
        i = 0
        for line in fin:
            count = int(line.strip().split()[1])
            if count >= 40:
                i += 1
                fout.write(line)
print i
            
