# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 21:56:45 2019

@author: Daniel Araújo Chaves Souza
"""
# -- importa a biblioteca de acesso aos pinos 
import RPi.GPIO as GPIO

class Bomba():
    def __init__(self):
        # Desabilita avisos
        GPIO.setwarnings(False)
        # Modo de numeração do pinos: GPIO
        GPIO.setmode(GPIO.BCM)
        # GPIO do rele que controla a bomba
        self.pin = 7
        # -- Define pino como saida
        GPIO.setup(pin, GPIO.OUT)
    # -- Liga a bomba
    def ligar(self):
        GPIO.output(self.pin, GPIO.HIGH)
        print("Bomba ligada")
        
    # -- Desdiga a bomba
    def desligar(self):
        GPIO.output(self.pin, GPIO.LOW)
        print("Bomba Desligada")
