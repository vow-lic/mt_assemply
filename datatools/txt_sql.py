#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 09:49:23 2018

@author: lic
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('txt_type_file',type = str ,help = 'the .txt type file(format \'kamer\tcount\n\') which you want load in database')
parser.add_argument('-o',type = str ,default = 'test.sql' ,help = 'the name of sql file which used to count kmer')
args = parser.parse_args()

filename = args.txt_type_file
sqlname = args.o


with open(filename,'r') as fin,open(sqlname,'w') as fout:
    cl = 0
    fout.write('''DROP TABLE IF EXISTS KMERCOUNT;
CREATE TABLE KMERCOUNT
(KMER CHAR(50) UNIQUE NOT NULL,
COUNT INT NOT NULL);
INSERT INTO KMERCOUNT (KMER,COUNT) VALUES''')
    for line in fin:
        cl += 1
        if cl == 20:
            cl = 0
            fout.seek(-1,1)
            fout.write(';\nINSERT INTO KMERCOUNT (KMER,COUNT) VALUES')
        inf = line.strip().split()
        kmer = inf[0]
        count = int(inf[1])
        fout.write("('%s',%d),"%(kmer,count))
    fout.seek(-1,1)
    fout.write(';')
        

        
    