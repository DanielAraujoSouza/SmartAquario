# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:29:53 2019

@author: Daniel Araújo Chaves Souza
"""
# imports
#import RPi.GPIO as GPIO
import time

## GPIO do servo que controlar o alimentador
#pin = 18
#
##Ajuste estes valores para obter o intervalo completo do movimento do servo
#deg_0_pulse   = 0.5 
#deg_180_pulse = 2.5
#f = 100.0
#
## Faca alguns calculos dos parametros da largura do pulso
#period = 1000/f
#k      = 100/period
#deg_0_duty = deg_0_pulse*k
#pulse_range = deg_180_pulse - deg_0_pulse
#duty_range = pulse_range * k
#
##Iniciar o pino gpio
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(servo_pin,GPIO.OUT)
#pwm = GPIO.PWM(servo_pin,f)
#pwm.start(0)

# calcula o ângulo a ser passado para o servo
#def set_angle(angle):
#        duty = deg_0_duty + (angle/180.0)* duty_range
#        pwm.ChangeDutyCycle(round(duty,4))
#        print(round(duty,4))

# Define o tipo de alimentação
def alimentar(modo):
    # abertura P
    if modo == 1:
        print ("Alimentação 1")
#        set_angle(int(70))
        time.sleep(2)
        print ("Alimentado")
#        set_angle(int(47))
    
    # abertura M   
    elif modo == 2:
        print ("Alimentação 2")
#        set_angle(int(70))
        time.sleep(3)
        print ("Alimentado")
#        set_angle(int(47))
    
    # abertura G
    elif modo == 3:
        print ("Alimentação 3")
#        set_angle(int(70))
        time.sleep(4)
        print ("Alimentado")
#        set_angle(int(47))
