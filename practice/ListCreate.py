#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wjq'

L = ['Hello' , 'World' , 18 , 'Apple' , None]

result = [ word.lower() for word in L if isinstance(word,str) ]

print(result)

