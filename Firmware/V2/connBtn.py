# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:18:12 2019

@author: Daniel Araújo Chaves Souza
"""
# Imports
# -- importa a biblioteca de acesso aos pinos 
import RPi.GPIO as GPIO
# -- importa controle do led conexão (Azul)
import connLed
from datetime import datetime
import time

class ConnBtn():
    def __init__(self):
        # Modo de numeração do pinos: GPIO
        GPIO.setmode(GPIO.BCM)
        # GPIO do botao conexão
        self.pin = 6
        # -- Define pino como entrada pull-up
        GPIO.setup (pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Registra funcoes de callback apos 3s de botao pressionado
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=reset, bouncetime=3000)
        self.horario = ""

    # Remove horario que o botao foi pressionado (Conexão estabelecida)
    def removerHorario(self):
        arquivo = open('btnTime.asa', 'w')
        arquivo.write("")
        arquivo.close()
        self.horario = ""
        
    # Grava horario que o botao foi pressionado
    def gravarHorario(self):
        timestamp = int(datetime.timestamp(datetime.now()))
        arquivo = open('btnTime.asa', 'w')
        arquivo.write(str(timestamp))
        arquivo.close()
        self.horario = timestamp

    # Informa o estado do modo de conexão (ativo: True; inativo: False)
    def connState(self):
        try:
            # Calcula diferença entre a hora atual e a hora do arquivo
            dif = int(datetime.timestamp(datetime.now()) - self.horario)
            # Se menor que 60 aquario aceita conexão
            if dif <= 60:
                return True
        except:
            pass

        return False
        
    # Callback quando botao é pressionado
    def reset(self):
        if not connState():
            gravarHorario()        
            while not connState():
                connLed.desligar()
                time.sleep(0.3)
                connLed.ligar()
                time.sleep(0.3)
            

