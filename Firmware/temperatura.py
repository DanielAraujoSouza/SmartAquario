# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:42:52 2019

@author: Daniel Araújo Chaves Souza
"""
## imports
import RPi.GPIO as gpio
import threading 
import ctypes
import os
import glob
import time 
   
class Temperatura(threading.Thread): 
    def __init__(self, conexao): 
        threading.Thread.__init__(self) 
        self.conexao = conexao
        self.delay = 10
        # Configurações do Sensor
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'
    
    def run(self): 
        # Publica valor da temperatura
        while True:
            valor = self.valor()
            print ("Temp: " + str(valor) + "\n")
            if valor != "":
                self.conexao.pub(self.conexao.client_id+"/sensores/temperatura",valor)
            # Define o intervalo envio
            time.sleep(self.delay)
        
    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
 
    def valor(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string)/1000.0
            return temp_c
        else:
            return ""
    
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
