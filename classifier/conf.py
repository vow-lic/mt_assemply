# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 09:53:14 2018

@author: licao
"""
import multiprocessing

host = 'localhost'
user = 'root'
password = 'mydata#1234'
threadmax = multiprocessing.BoundedSemaphore(20)
