#-*- encoding: utf-8 -*-
'''
test.py
Created on 2020/3/30 15:41
Copyright (c) 2020/3/30, finch_xu.
@author: finch_xu
'''

from translate.tools import pocount
state = pocount.calcstats_old("convert/20200329173855-doles.po")
print(state["total"])