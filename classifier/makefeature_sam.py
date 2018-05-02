# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 12:01:57 2018

@author: licao
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('sam_type_file',type = str ,help = 'the sam_type file which you want extact features from it')
parser.add_argument('--dbname',type = str ,default = 'kmer_count.db' ,help = 'the name of database which used to count kmer')
parser.add_argument('-o','--outfile',type = str ,help = 'the name of output file')
parser.add_argument('-k','--kmer',type = int ,default = 31 ,help = 'the length of kmer')
args = parser.parse_args()
filename = args.sam_type_file
dbname = args.dbname
outfile = args.outfile
K = args.kmer

from file_dict import sam_extract
from seq2list import seq_count_triplet
from seq2list import seq_kmer_cal
import multiprocessing
pool_size = multiprocessing.cpu_count()


def write_features_svm(tuple_source_seq,k=K,dbname=dbname):
    source = tuple_source_seq[0]
    seq = tuple_source_seq[1]
    if source == '':
        source = 0
    elif source == 'MT':
        source = 1
    else:
        source = -1
    kmerlist = seq_kmer_cal(seq,dbname,k)
    triplist = seq_count_triplet(seq)
    writelist = kmerlist + triplist
    ww = str(source)
    for i in range(len(writelist)):
        ww += ' %d:%f'%(i+1,writelist[i])
    ww += '\n'
    return ww

seqlist = sam_extract(filename)
print 'seqlist created'

pool = multiprocessing.Pool(processes=pool_size)
pool_outputs = pool.map(write_features_svm,seqlist)
pool.close()
pool.join()

with open(outfile,'w') as fout:
    for line in pool_outputs:
        fout.write(line)