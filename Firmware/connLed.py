# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 12:25:28 2019

@author: Daniel Araújo Chaves Souza
"""
# -- importa a biblioteca de acesso aos pinos 
import RPi.GPIO as GPIO

class ConnLed():
    def __init__(self): 
        # Desabilita avisos
        GPIO.setwarnings(False)
        # Modo de numeração do pinos: GPIO
        GPIO.setmode(GPIO.BCM)
        # GPIO do led conexão (azul)
        self.pin = 5
        # -- Define pino como saida
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    # -- Liga o Led
    def ligar(self):
        GPIO.output(self.pin, GPIO.HIGH)
        print("connLed ON")

    # -- desdiga o Led
    def desligar(self):
        GPIO.output(self.pin, GPIO.LOW)
        print("connLed OFF")
