# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 10:51:51 2019

@author: Daniel Araújo Chaves Souza
"""
#Define Libraries
#import RPi.GPIO as gpio
import threading 
import ctypes
import time 
   
class estado(threading.Thread): 
    def __init__(self, modo): 
        threading.Thread.__init__(self) 
        self.modo = modo
        #Configuring don’t show warnings 
#        gpio.setwarnings(False)
        
        #Configuring GPIO
#        pinBlue = 17
#        pinRed = 24
#        pinGreen = 27
#        
#        gpio.setmode(gpio.BCM)
#        gpio.setup(pinBlue,gpio.OUT)
#        gpio.setup(pinRed,gpio.OUT)
#        gpio.setup(pinGreen,gpio.OUT)
        
        #Configure the pwm objects and initialize its value
#        self.pwmBlue = gpio.PWM(pinBlue,120)
#        self.pwmBlue.start(0)
#        
#        self.pwmRed = gpio.PWM(pinRed,120)
#        self.pwmRed.start(0)
#        
#        self.pwmGreen = gpio.PWM(pinGreen,120)
#        self.pwmGreen.start(0)
        
    def run(self): 
        if self.modo == 1:
            print ("Azul Ligado")
#            self.pwmBlue.ChangeDutyCycle(100)
#            self.pwmRed.ChangeDutyCycle(0)
#            self.pwmGreen.ChangeDutyCycle(0)
        # Vermelho
        elif self.modo == 2:
            print("Vermelho Ligado")
#            self.pwmBlue.ChangeDutyCycle(0)
#            self.pwmRed.ChangeDutyCycle(100)
#            self.pwmGreen.ChangeDutyCycle(0)
        # Verde
        elif self.modo == 3:
            print ("Verde Ligado")
#            pwmBlue.ChangeDutyCycle(0)
#            pwmRed.ChangeDutyCycle(0)
#            pwmGreen.ChangeDutyCycle(100)
        
        # Especial1
        elif self.modo == 4:
            while True:
                print ("a")
                time.sleep(0.5)
                print ("b")
                time.sleep(0.5)
        # Desligado
        else:
            print ("Desligado")
#            self.pwmBlue.ChangeDutyCycle(0)
#            self.pwmRed.ChangeDutyCycle(0)
#            self.pwmGreen.ChangeDutyCycle(0)
           
    def get_id(self): 
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id
   
    def stop(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
              ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure') 
       

