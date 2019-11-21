# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 21:56:45 2019

@author: Daniel Araújo Chaves Souza
"""
## -- importa a biblioteca de acesso aos pinos 
#import RPi.GPIO as GPIO
## Modo de numeração do pinos: GPIO
#GPIO.setmode(GPIO.BMC)
#
## GPIO do rele que controla a bomba
#pin = 12
## -- Define pino como saida
#GPIO.setup(pin, GPIO.OUT)
# -- Liga a bomba
def ligar():
    #GPIO.output(pin, GPIO.HIGH)
    print("Bomba ligada")
    
# -- desdiga a bomba
def desligar():
    #GPIO.output(pin, GPIO.LOW)
    print("Bomba Desligada")