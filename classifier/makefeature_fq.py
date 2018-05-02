# -*- coding: utf-8 -*-
"""
@author: licao
"""
#接受命令行参数
import argparse 
parser = argparse.ArgumentParser()
parser.add_argument('fq_type_file',type = str ,help = 'the fq_type file which you want extact features from it')
parser.add_argument('--dbname',type = str ,default = 'kmer_count.db' ,help = 'the name of database which used to count kmer')
parser.add_argument('-o','--outfile',type = str ,help = 'the name of output file')
parser.add_argument('-k','--kmer',type = int ,default = 31 ,help = 'the length of kmer')
args = parser.parse_args()
filename = args.fq_type_file
dbname = args.dbname
outfile = args.outfile
K = args.kmer

#从file_dict.py和seq2list.py文件中引入需要使用的函数
from file_dict import fq_extract
from seq2list import seq_count_triplet
from seq2list import seq_kmer_cal

#引入多进程程代码包，确定进程数
import multiprocessing
pool_size = multiprocessing.cpu_count()

#定义由测序序列生成特征值的函数
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

#使用函数从fq文件中提取测序序列
seqlist = fq_extract(filename)
print 'sequence list created'

#利用提取序列及已定义生成特征值函数创建多进程并运行
pool = multiprocessing.Pool(processes=pool_size)
pool_outputs = pool.map(write_features_svm,seqlist)
pool.close()
pool.join()

#将以上步骤产生的特征值结果写入文件
with open(outfile,'w') as fout:
    for line in pool_outputs:
        fout.write(line)