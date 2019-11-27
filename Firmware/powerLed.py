# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:22:26 2019

@author: Daniel Araújo Chaves Souza
"""
# -- importa a biblioteca de acesso aos pinos 
import RPi.GPIO as GPIO

class PowerLed():
    def __init__(self): 
        # Desabilita avisos
        GPIO.setwarnings(False)
        # Modo de numeração do pinos: GPIO
        GPIO.setmode(GPIO.BCM)
        # GPIO do led power (Verde)
        self.pin = 12
        # -- Define pino como saida
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    # -- Liga o Led
    def ligar(self):
        GPIO.output(self.pin, GPIO.HIGH)
        print("powerLed ON")

    # -- desdiga o Led
    def desligar(self):
        GPIO.output(self.pin, GPIO.LOW)
        print("powerLed OFF")

