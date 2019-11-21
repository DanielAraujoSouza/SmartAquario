# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 12:25:28 2019

@author: Daniel Araújo Chaves Souza
"""
# -- importa a biblioteca de acesso aos pinos 
import RPi.GPIO as GPIO
# Modo de numeração do pinos: GPIO
GPIO.setmode(GPIO.BCM)

# GPIO do led conexão (azul)
pin = 12
# -- Define pino como saida
GPIO.setup(pin, GPIO.OUT)
# -- Liga o Led
def ligar():
    GPIO.output(pin, GPIO.HIGH)
    print("connLed ON")
# -- desdiga o Led
def desligar():
    GPIO.output(pin, GPIO.LOW)
    print("connLed OFF")