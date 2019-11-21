# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:22:26 2019

@author: Daniel Araújo Chaves Souza
"""
# -- importa a biblioteca de acesso aos pinos 
import RPi.GPIO as GPIO
# Modo de numeração do pinos: GPIO
GPIO.setmode(GPIO.BCM)

# GPIO do led power (Verde)
pin = 12
# -- Define pino como saida
GPIO.setup(pin, GPIO.OUT)
# -- Liga o Led
def ligar():
    GPIO.output(pin, GPIO.HIGH)
    print("powerLed ON")
# -- desdiga o Led
def desligar():
    GPIO.output(pin, GPIO.LOW)
    print("powerLed OFF")