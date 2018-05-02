# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 09:49:23 2018

@author: lic
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('sam_file',type = str ,help = 'perfileter sam type file ')
parser.add_argument('-o',type = str ,default = 'filter.sam' ,help = 'the name of output fq file ')
parser.add_argument('-chro',type = str ,default = 'MT' ,help = 'chr extracted ')
args = parser.parse_args()

finname = args.sam_file
foutname = args.o
chro = args.chro
a = 0
with open(finname,'r') as fin , open(foutname,'w') as fout:
    for line in fin:
        if line.startswith('@'):
            continue
        else:
            inf = line.strip().split()
            head = inf[0]
            source = inf[2]
            seq = inf[9]
            quality = inf[10]
            if source == chro:
                a += 1
                fout.write('@%s\n%s\n+\n%s\n'%(head,seq,quality))
print a
