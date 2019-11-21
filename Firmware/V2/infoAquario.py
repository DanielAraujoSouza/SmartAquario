# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:33:11 2019

@author: Daniel Araújo Chaves Souza
"""

class infoAquario():
  def __init__(self)
    # Cria um identificador unico para o dispositivo:
    cpuserial = "0000000000000000"
    try:
      f = open('/proc/cpuinfo','r')
      for line in f:
        if line[0:6]=='Serial':
          cpuserial = line[10:26]
      f.close()
    except:
      cpuserial = "ERROR000000000"
    self.aquarioId =  "SmarthAquario-"+str(cpuserial)
    
    # Identificador do app que esta conectado ao aquario
    try:
      arquivo = open('appid.asa', 'r')
      self.appId = arquivo.readline().strip()
      arquivo.close()
    except:
      self.appId = ""

  # Grava o identificador do app no arquivo
  def appIdWrite(self,id):
      try:
          arquivo = open('appid.asa', 'w')
          arquivo.write(str(id))
          arquivo.close()
          self.appId = str(id)
      except:
          self.appId = ""
