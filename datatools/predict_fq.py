#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 14:20:03 2018

@author: lic
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-fq',type = str ,nargs=2,help = 'the .fq type file which you want extract')
parser.add_argument('--predict',type = str ,nargs=2,help = 'the libsvm svm-predict output file')
parser.add_argument('-o',type = str ,nargs=2,help = 'the file name of output')
args = parser.parse_args()

finname1 = args.fq[0]
finname2 = args.fq[1]
predict1 = args.predict[0]
predict2 = args.predict[1]
foutname1 = args.o[0]
foutname2 = args.o[1]

def extract_predict_file(filename):
    predictlist = []
    with open(filename,'r') as fin:
        for line in fin:
            predictlist.append(int(line.strip()))
    return predictlist

def write_fq_pair(list1,list2,finname,foutname):
    with open(finname,'r') as fin,open(foutname,'w') as fout:
        i = 0
        writer = 0
        for line in fin:
            if line.startswith('@'):
                if list1[i] == 1 or list2[i] == 1:
                    writer = 1
                    fout.write(line)
                else:
                    writer = 0
                i += 1
            elif writer:
                fout.write(line)
    return 

list1 = extract_predict_file(predict1)
list2 = extract_predict_file(predict2)
assert len(list1) == len(list2)
print len(list1),'|',len(list2)

low = 0 
uper = 0
for a in range(len(list1)):
    if list1[a] == 1 and list2[a] == 1:
        low += 1
    if list1[a] == 1 or list2[a] == 1:
        uper += 1

print list1.count(1),'|',list2.count(1),'|',low,'|',uper

write_fq_pair(list1,list2,finname1,foutname1)
write_fq_pair(list1,list2,finname2,foutname2)
