#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 14:08:08 2018

@author: lic
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('fq_type_file',nargs='+',type = str ,help = 'the fq_type file which you want extact features from it')
parser.add_argument('-o','--outfile',type = str ,help = 'the name of output file')
parser.add_argument('-k','--kmer',type = int ,default = 31 ,help = 'the length of kmer')
parser.add_argument('-contig_len',type = int ,default = 151 )
parser.add_argument('-kmer_cov',type = int ,default = 1 )
args = parser.parse_args()
filename = args.fq_type_file
outfile = args.outfile
K = args.kmer
min_len = args.contig_len
min_cov = args.kmer_cov

def fq_merge(filenametuble,outfile = 'all.fq'):
    fout = open(outfile,'w')
    for names in filenametuble:
        fin = open(names,'r')
        for line in fin:
            fout.write(line)
        fin.close()
    fout.close()
    return outfile


def mk_kmer_dict(dress,k):
    from string import maketrans
    kmer_dict = {}
    heads = []
    with open(dress,'r') as fin:
        trantab = maketrans('ATCG','TAGC')
        at_pass = 0
        for line in fin:
            if line.startswith('@'):
                tatle = line.strip().split()[0][1:]
                at_pass = 1
            elif at_pass:
                seq = line.strip()
                if 'N' not in seq and len(seq) > k:
                    heads.append(seq[:k])
                    for i in range(len(seq)-k+1):
                        kmer = seq[i:i+k]
                        kmer_1 = kmer[:-1]
                        try:
                            kmer_dict[kmer_1].append(kmer[-1])
                        except KeyError:
                            kmer_dict[kmer_1] = [kmer[-1]]
                    reseq = seq[::-1].translate(trantab)
                    heads.append(reseq[:k])
                    for i in range(len(reseq)-k+1):
                        kmer = reseq[i:i+k]
                        kmer_1 = kmer[:-1]
                        try:
                            kmer_dict[kmer_1].append(kmer[-1])
                        except KeyError:
                            kmer_dict[kmer_1] = [kmer[-1]]
                at_pass = 0
    cl_kmer_dict = {}
    for k,v in kmer_dict.items():
        if len(v) >= min_cov:
            atcg = []
            atcg.append(v.count('A'))
            atcg.append(v.count('T'))
            atcg.append(v.count('C'))
            atcg.append(v.count('G'))
            cl_kmer_dict[k] = [('A','T','C','G')[atcg.index(max(atcg))],len(v)]
#    print len(cl_kmer_dict)
    return cl_kmer_dict,heads

def head_filter(heads,t_kmerdict,k):
    kmerdict = t_kmerdict.copy()
    contigdict = {}
    Cyclization = False
    for head in heads:
        usedkmer = {}
        contig = head 
        try:
            if kmerdict[contig[:-1]][0] == contig[-1]:
                score = kmerdict[contig[:-1]][1]
                while 1:#len(contig) < 20000:
                    key = contig[-k:]
                    try:
                        if len(contig) - usedkmer[key] > 15000:
                            contig = contig[usedkmer[key]-k+1:len(contig)]
                            Cyclization = True
                        for i in usedkmer.keys():
                            kmerdict.pop(i[1:])
                        break
                    except KeyError:
                        try:
                            contig += contigdict[key][0][k:]
                            score += contigdict[key][1]
                            #contigdict.pop(key)
                        except KeyError:
                            try:
                                usedkmer[key] = len(contig)
                                contig += kmerdict[key[1:]][0]
                                score +=  kmerdict[key[1:]][1]
                                kmerdict.pop(key[1:])
                            except KeyError:
                                break
                contigdict[head] = [contig,score]
#        threshold
        except KeyError:
            continue
    if Cyclization :
        print 'Cyclization complete'
    else:
        print 'Cyclization failed'
    transcript = []
    candidate = []
    for contig,score in contigdict.values():
        L = len(contig)
        if L >= min_len:
            transcript.append(score)
            candidate.append(contig)
    num = 1
    maxnum = len(transcript)
    trails = []
    while num <= maxnum:
        sel_ind = transcript.index(max(transcript))
        trails.append(candidate[sel_ind][:k])
        transcript[sel_ind] = 0
        num += 1
    return trails


def assembly(heads,t_kmerdict,k):
    kmerdict = t_kmerdict.copy()
    contigdict = {}
    for head in heads:
        contig = head 
        try:
            if kmerdict[contig[:-1]][0] == contig[-1]:
                score = kmerdict[contig[:-1]][1]
                while 1:#len(contig) < 20000:
                    key = contig[-k:]
                    if contigdict.__contains__(key):
                        contig += contigdict[key][0][k:]
                        score += contigdict[key][1]
                        #contigdict.pop(key)
                    else:
                        try:
                            contig += kmerdict[key[1:]][0]
                            score +=  kmerdict[key[1:]][1]
                            kmerdict.pop(key[1:])
                        except KeyError:
                            break
                contigdict[head] = [contig,score]
#        threshold
        except KeyError:
            continue
    return contigdict

if type(filename) == str:
    kmer,headlist = mk_kmer_dict(filename,K)
else:
    filemerge = fq_merge(filename)
    kmer,headlist = mk_kmer_dict(filemerge,K)
print '|',len(kmer),len(headlist)
tails = headlist#head_filter(headlist,kmer,K)
print '|',len(kmer),len(tails)
contigs = assembly(tails,kmer,K)
print '|',len(contigs)
lengths = []
transcript = []
candidate = []

for contig,score in contigs.values():
    L = len(contig)
    if L >= min_len:
        lengths.append(L)
        transcript.append(score)
        candidate.append(contig)
lengths_set = list(set(lengths))
lengths_set.sort()
for i in lengths_set:
    print i,lengths.count(i)

num = 1
maxnum = len(transcript)
fout = open(outfile,'w')
while num <= maxnum:
    sel_ind = transcript.index(max(transcript))
    sel_sco = transcript[sel_ind]
    sel_seq = candidate[sel_ind]
    sel_len = len(sel_seq)
    s = 0
    fout.write('>%d_%d_%d\n'%(num,sel_len,sel_sco))
    while s+60 < sel_len:
        fout.write('%s\n'%sel_seq[s:s+60])
        s += 60
    fout.write('%s\n'%sel_seq[s:])
    num += 1
    transcript[sel_ind] = 0
fout.close()



