# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:33:11 2019

@author: Daniel Araújo Chaves Souza
"""
# Cria um identificador unico para o dispositivo
def id():
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
    
  return "SmarthAquario-"+str(cpuserial)

# recupero Id do app se estiver vinculado
def appId():
    try:
        arquivo = open('appid.asa', 'r')
        nome = arquivo.readline().strip()
        arquivo.close()
    except (FileNotFoundError):
        nome = ""
    return nome

# Grava o identificador do app no arquivo
def appIdWrite(id):
    try:
        arquivo = open('appid.asa', 'w')
        arquivo.write(str(id))
        arquivo.close()
    except:
        pass