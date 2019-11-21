# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:06:00 2019

@author: Daniel Araújo Chaves Souza
"""
# imports
import RPi.GPIO as GPIO
import threading 
import ctypes
import time 

class Nivel(threading.Thread): 
    def __init__(self, conexao): 
        threading.Thread.__init__(self) 
        self.conexao = conexao
        self.delay = 30
        # Configurando os GPIO
        GPIO.setmode (GPIO.BCM)
        self.pin = 13
        # -- Define como pull-up
        GPIO.setup (self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
    
    def run(self): 
        while True:
            valor = self.valor()        
            # Publica valor do nivel
            print ("Nivel: " + str(valor) + "\n")
            #self.conexao.pub(self.conexao.client_id+"/sensores/nivel/valor",valor)        
            # Define o intervalo envio
            time.sleep(self.delay)

    def valor(self ):
        return GPIO.input(self.pin)

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
