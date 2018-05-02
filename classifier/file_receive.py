# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 09:53:14 2018

@author: licao
"""

def sam_extract(adress):
    samlist = []#[(source,seq)]
    fin = open(adress,'r')
    for line in fin:
        if line.startswith('@'):
            continue
        else:
            inf = line.strip().split()
#            head = inf[0]
            source = inf[2]
            seq = inf[9].replace('N','')
            samlist.append((source,seq))
    fin.close()
    print 'len(samlist)=%d'%len(samlist)
    return samlist

def fq_extract(adress):
    fqlist = []
    fin = open(adress,'r')
    at_pass = 0
    for line in fin:
        if line.startswith('@'):
#            head = line.strip().split()[0][1:]
            at_pass = 1
        elif at_pass:
            fqlist.append(('',line.strip().replace('N','')))
            at_pass = 0
    fin.close()
    print 'len(fqlist)=%d'%len(fqlist)
    return fqlist

if __name__ == '__main__':
    seqlist = sam_extract('test.sam')
    print seqlist
    
    fqlist = fq_extract('test.fq')
    print fqlist
    
