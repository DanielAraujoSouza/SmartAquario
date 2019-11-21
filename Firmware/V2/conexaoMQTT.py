# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:38:12 2019

@author: Daniel Araújo Chaves Souza
"""
# Imports
# -- importa biblioteca do eclipse paho
import paho.mqtt.client as mqtt
# -- importa informaçõe do aquario
from infoAquario import InfoAquario
# -- importa controle do led conexão (Azul)
from connLed import ConnLed
# -- importa rotina do botao de reset
from connBtn import ConnBtn
# -- importa controle da bomba
from bomba import Bomba
# -- importa controle de iluminação
from iluminacao import Iluminacao
# -- importa controle de alimentação
from alimentacao import Alimentacao
# -- importa temporizador
import time
# -- importa bibioteca json
import json

class ConexaoMQTT():
    def __init__(self):
        # Cria uma flag de conexão
        self.connected_flag = False
        # Cria uma flag de desconexão
        self.disconnect_flag = False
        # Ativa os logs
        self.mqttclient_log = False
        # Thread de controle de iluminação
        self.thrIlum = Iluminacao(0)
        # Led de conexão
        self.connLed = ConnLed()
        # Botão de conexão
        self.connBtn = ConnBtn()
        # Informações do aquario
        self.infoAquario = InfoAquario()
        # Bomba de água (Relé)
        self.bomba = Bomba()
        # Alimentacao
        self.alimentacao = Alimentacao()
        
        # Variaveis de Conexão
        self.broker = "44.227.11.98"
        self.port = 1883
        #self.usuario = ""
        #self.senha = ""
        self.client_id = self.infoAquario.aquarioId
        print(self.client_id)
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_log = self.on_log

    def on_connect(self, client, obj, flags, rc):
            print ("on")
            if rc == 0:
                # Conexão bem sucedida
                self.connected_flag = True
                # Liga led de conexão
                self.connLed.ligar()
                print("Conexão Estabelecida")

            else:
                self.connLed.desligar()
                print("Errod de conexão=",rc)

    def on_disconnect(self, client, userdata, rc):
        print("motivo da desconexão" + str (rc))
        self.connLed.desligar()
        self.connected_flag = False
        self.disconnect_flag = True

    def on_message(self, client, userdata, message):
        
        topico = message.topic
        payload = json.loads(str(message.payload.decode("utf-8")))
        print(payload)
        remetente = payload["APPID"]
        msg = payload["MSG"]
        
        print ("topico: " + topico)
        print ("remetente: " + remetente)
        print ("msg: " + msg)
        print("era pra ser" + self.client_id + "/conectar")
        print(self.connBtn.connState())
        
        if topico == self.client_id+"/conectar":    
            print("entif")            
            if not self.connBtn.connState():
                # Se o botao de conexão não foi pressionado a menos de 60s
                print("connStateerro")
                self.pub(remetente + "/conectar/resposta", "ERRO")
            elif remetente != "":
                print("vai confirar")
                # Confirma conexão
                self.pub(remetente+"/conectar/resposta", self.client_id)
                # Grava id do app
                print ("vai gravar")
                self.infoAquario.appIdWrite(remetente)
                # Remove horario do arquivo indicando que a conexão foi estabelecida
                print("remover horario")
                self.connBtn.removerHorario()

        # So aceita mensagens do app vinculado
        elif self.infoAquario.appId != "" and remetente == self.infoAquario.appId:
            # Topico para bomba (Relé)
            if topico == (self.infoAquario.appId+"/atuadores/bomba"):
                if msg == "ligar":
                    self.bomba.ligar()
                elif msg == "desligar":
                    self.bomba.desligar()
            
            # Topico iluminação (Fita de Led)
            elif topico == (self.infoAquario.appId+"/atuadores/iluminacao"):
                cor = json.loads(msg)
                if cor["MODO"] == "cor":
                    self.thrIlumState(cor["MODO"],cor["R"],cor["G"],cor["B"])
                   
                elif cor["MODO"] == "especial":
                    self.thrIlumState(cor["MODO"],cor["TIPO"])
                           
            # Topico alimentação
            elif topico == (self.infoAquario.appId+"/atuadores/alimentacao"):
                if msg == "P":
                    self.alimentacao.alimentar(1)
                   
                elif msg == "M":
                    self.alimentacao.alimentar(2)
                   
                elif msg == "G":
                    self.alimentacao.alimentar(3)

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, client, userdata, level, buf):
        if self.mqttclient_log:
            print(buf)

    def iniciar(self):
        self.connect("mqtt.eclipse.org", 1883, 60)
        self.subscribe("$SYS/#", 0)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc

    def thrIlumState(self, modo,r="",g="",b=""):
        # Para a thread se ela estiver executando
        if self.thrIlum.is_alive():
            print("Parando thrIlum")
            self.thrIlum.stop()
        # Inicia um nova thread com o novo estado
        self.thrIlum = Iluminacao(modo)
        self.thrIlum.start()
    def iniciar(self):
        # Credenciais de acesso
        #self.client.username_pw_set(username=usuario,password=senha) 
        # Inicia o loop em uma nova Thread 
        self.client.loop_start()
        # Conecta ao Broker
        self.client.connect(self.broker,self.port)
        # Loop que aguarda a conexão
        while not self.connected_flag:
            print("Aguardando Conexão")
            time.sleep(5)
        return True
   
    def parar(self):
        self.client.loop_stop()
        self.client.disconnect()
        if self.thrIlum.is_alive():
            print("matando thread")
            self.thrIlum.stop()

    def sub(self,topico):
        if self.connected_flag:
            self.client.subscribe(topico,1)
        else:
            print("Falha de publicação: Sem conexão")

    def pub (self,topico, msg):
        print("fpub")
        print(self.connected_flag)
        if self.connected_flag:
            payload = {"SAID":self.client_id,
                       "MSG":msg
                       }
            print(payload)
            self.client.publish(topico,json.dumps(payload),1)
            print("publicou")
        else:
            print("Falha de publicação: Sem conexão")


