# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 12:15:53 2019

@author: Admin
"""

#import teste2
#
#ds = "d"
#def ch():
#    global ds
#    ds = "e"
#ch()
#print (ds)    
#while not teste2.var:
#    print("ok")
#    teste2.change()


#from datetime import datetime
#import time
##timestamp1 = datetime.timestamp(datetime.now())
##timestamp = int(timestamp1)
##arquivo = open('btnTime.asa', 'w')
##arquivo.write(str(timestamp))
##arquivo.close()
#
##try:
##    arquivo = open('usuario.ll', 'r')
##    print(datetime.fromtimestamp(int(arquivo.read())))
##    arquivo.close()
##except:
##    print("erro")
#try:
#    arquivo = open('btnTime.asa', 'r')
#    valor = int(arquivo.readline().strip())
#    arquivo.close()
#    # Calcula diferença entre a hora atual e a hora do arquivo
#    dif = int(datetime.timestamp(datetime.now()) - valor)
#    print(dif)
#    if dif <= 30:
#        print(True)
#except:
#    pass
#
#    print(False)
for i in range(10):
    print(i)
    if i ==3:
        break