# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 09:49:23 2018

@author: lic
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('sam_file',type = str ,help = 'perfileter sam type file ')
parser.add_argument('-o',type = str ,default = 'filter.sam' ,help = 'the name of output file ')
args = parser.parse_args()

finname = args.sam_file
foutname = args.o

with open(finname,'r') as fin,open(foutname,'w') as fout:
    mtc = 0
    allc = 0
    w = 0
    writec = 0
    for line in fin:
        if line.startswith('@'):
            fout.write(line)
        else:
            allc += 1
            inf = line.strip().split()
            source = inf[2]
            if source == 'MT':
                mtc += 1
                writec += 1
                fout.write(line)
                w += 1
            else:
                if writec > 0:
                    writec -= 1
                    fout.write(line)
                    w += 1
    fin.close()

print allc,'|',mtc,'|',w



