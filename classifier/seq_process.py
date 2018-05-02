# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 09:53:14 2018

@author: licao
"""
import numpy
import pymysql
from conf import host,user,password

def seq_count_triplet(seq):
    triplist = ['AAA', 'AAT', 'AAC', 'AAG', 'ATA', 'ATT', 'ATC', 'ATG', 'ACA', 'ACT', 'ACC', 'ACG', 'AGA', 'AGT', 'AGC', 'AGG', 'TAA', 'TAT', 'TAC', 'TAG', 'TTA', 'TTT', 'TTC', 'TTG', 'TCA', 'TCT', 'TCC', 'TCG', 'TGA', 'TGT', 'TGC', 'TGG', 'CAA', 'CAT', 'CAC', 'CAG', 'CTA', 'CTT', 'CTC', 'CTG', 'CCA', 'CCT', 'CCC', 'CCG', 'CGA', 'CGT', 'CGC', 'CGG', 'GAA', 'GAT', 'GAC', 'GAG', 'GTA', 'GTT', 'GTC', 'GTG', 'GCA', 'GCT', 'GCC', 'GCG', 'GGA', 'GGT', 'GGC', 'GGG']
    seqlist = []
    tripcount = []
    L = len(seq) - 2
    for i in range(L):
        seqlist.append(seq[i:i+3])
    for tri in triplist:
        tripcount.append(float(seqlist.count(tri))/float(L))
    return tripcount

def seq_kmer_cal(seq,dbname,k = 31):  
    db = pymysql.connect(host,user,password,dbname)
    countlist = []
    for i in range(len(seq)-k+1):
        kmer = seq[i:i+k]
        db.ping(True)
        cur = db.cursor()
        cur.execute("SELECT COUNT FROM KMERCOUNT WHERE KMER = '%s';"%kmer)
        COUNT = ''
        rows = cur.fetchall()
        for row in rows:
            COUNT = row[0]
        if COUNT:
            countlist.append(COUNT)
    l = len(countlist)
    if l == 0:
        s = 0
        v = 0
    else:
        s = numpy.sum(countlist)
        v = numpy.var(countlist)
    kmercal = [l,s,v]
    db.close()
    return kmercal


if __name__ == '__main__':
    #from file_dict import sam_extract,sql_count_kmer
    #seqlist = sam_extract('test.sam')
    #print seqlist

    #kmerabundance = sql_count_kmer(seqlist,dbname = 'test.db')
    
    
    #a = 144242424123143313424313142431242231433134212231424312412143313424123142431241231422134241431424212412314331342412314243124423141313424113142421241231L
    #tri = seq_n_count_triplet(a)
    #print tri
    
    #kcal = seq_n_kmer_cal(a,'test.db')
    #print kcal
    
    b = 'CCGGCACAAGTTGAAAGGGCCTCGATAGGGTAAATGGGTAGCCATGCATGTCTCTGGCACCGGTGGGTCGTGGAACTTAAAGGGGTGCTGTCCTTACCGTCTGCCTGGCAGGGTTTCAAGTGATGTTCATGGAGTTCCCTTATGCCAGGA'
    kcal = seq_kmer_cal(b,'test.db')
    print kcal

