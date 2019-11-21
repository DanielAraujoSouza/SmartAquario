# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:20:33 2019

@author: Daniel Araújo Chaves Souza
"""
# Imports
# -- importa a biblioteca de acesso aos pinos 
import RPi.GPIO as GPIO
# -- importa conexao MQTT
import conexaoMQTT
# -- importa controle do led power (Verde)
from powerLed import PowerLed
# -- importa controle de Temperatura
import temperatura
# -- importa controle de nivel
import nivel
# -- importa temporizador
import time

## Define parametro de gpio
GPIO.setwarnings(False)
GPIO.cleanup()

#try:
# Liga luz de power ON
power_led = PowerLed()
power_led.ligar()

# Conecta ao Broker
conexao = conexaoMQTT()

if(not conexao.iniciar()):
    print("Erro de Conexão")
    conexao.parar()
    exit()

# Inscreve-se nos topicos de atuação/conexão
conexao.sub(conexao.client_id+"/atuadores/bomba")
conexao.sub(conexao.client_id+"/atuadores/iluminacao")
conexao.sub(conexao.client_id+"/atuadores/alimentacao")
conexao.sub(conexao.client_id+"/conectar")

# Inicia Threads dos sensores
thrTemp = temperatura.tmpSensor(conexao)
thrTemp.start()
thrNivel = nivel.lvlSensor(conexao)
thrNivel.start()


# Monitora se as threads de envio estão rodando
while True:
    if not thrTemp.is_alive():
        thrTemp = temperatura.tmpSensor(conexao)
        thrTemp.start()
        
    if not thrNivel.is_alive():
        thrNivel = nivel.lvlSensor(conexao)
        thrNivel.start()
    # Define o intervalo de 10s
    time.sleep(10)
#except:
print ("Encerrando...")
GPIO.cleanup()
conexao.parar()
try:
    thrTemp.stop()
    thrNivel.stop()
except:
    pass
       
#    exit()
