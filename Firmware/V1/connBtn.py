# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:18:12 2019

@author: Daniel Araújo Chaves Souza
"""
## Imports
## -- importa a biblioteca de acesso aos pinos 
#import RPi.GPIO as GPIO
## -- importa controle do led conexão (Azul)
#import connLed
#from datetime import datetime
#import time
#
## Remove horario que o botao foi pressionado (Conexão estabelecida)
#def removerHorario():
#    arquivo = open('btnTime.asa', 'w')
#    arquivo.write("")
#    arquivo.close()
#    
## Grava horario que o botao foi pressionado
#def gravarHorario():
#    timestamp = int(datetime.timestamp(datetime.now()))
#    arquivo = open('btnTime.asa', 'w')
#    arquivo.write(str(timestamp))
#    arquivo.close()
#
## Informa o estado do modo de conexão (ativo: True; inativo: False)
#def connState():
#    try:
#        arquivo = open('btnTime.asa', 'r')
#        valor = int(arquivo.readline().strip())
#        arquivo.close()
#        # Calcula diferença entre a hora atual e a hora do arquivo
#        dif = int(datetime.timestamp(datetime.now()) - valor)
#        
#        if dif <= 60:
#            return True
#    except:
#        pass
#
#    return False
#    
## Callback quando botao é pressionado
#def reset():
#    if not connState():
#        gravarHorario()        
#        while not connState():
#            connLed.desligar()
#            time.sleep(0.3)
#            connLed.ligar()
#            time.sleep(0.3)
#            
#
## Modo de numeração do pinos: GPIO
#GPIO.setmode(GPIO.BMC)
#
## GPIO do led power (Verde)
#pin = 6
#
## -- Define pino como entrada pull-up
#GPIO.setup (pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
## Registra funcoes de callback apos 5s de botao pressionado
#GPIO.add_event_detect(pin, GPIO.FALLING, callback=reset, bouncetime=5000)