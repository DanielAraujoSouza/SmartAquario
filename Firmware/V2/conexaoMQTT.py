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
import alimentacao
# -- importa temporizador
import time
# -- importa bibioteca json
import json

class ConexaoMQTT(mqtt.Client):
    def __init__(self):
        self.client_id = self.infoAquario.appId
        self.client = mqtt.Client(self.client_id)
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
        infoAquario = InfoAquario()
        # Bomba de água (Relé)
        bomba = Bomba() 

    def on_connect(self, client, obj, flags, rc):
            if rc == 0:
                # Conexão bem sucedida
                self.client.connected_flag = True
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
        remetente = payload["APPID"]
        msg = payload["MSG"]
        
        if topico == (self.infoAquario.appId+"/conectar"):
            if self.connBtn.connState():
                # Se o botao de conexão não foi pressionado a menos de 60s
                pub(self.client_id+"/conectar/resposta", "ERRO")
            elif remetente != "":
                # Confirma conexão
                pub(self.client_id+"/conectar/resposta", client_id)
                # Grava id do app
                self.infoAquario.appIdWrite(remetente)
                # Remove horario do arquivo indicando que a conexão foi estabelecida
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
                    alimentacao.alimentar(1)
                   
                elif msg == "M":
                    alimentacao.alimentar(2)
                   
                elif msg == "G":
                    alimentacao.alimentar(3)

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, client, userdata, level, buf):
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


#####################
    
def on_message(client, userdata, message):
    # Objeto global da Thread de iluminação
    global thrIlum
    # Identificador do app vinculado ao aquário
    global app_id
    
    topico = message.topic
    payload = json.loads(str(message.payload.decode("utf-8")))
    remetente = payload["APPID"]
    msg = payload["MSG"]
    
    if topico == (self.infoAquario.appId+"/conectar"):
        if connBtn.connState():
            # Se o botao de conexão não foi pressionado a menos de 60s
            pub(client_id+"/conectar/resposta", "ERRO")
        elif remetente != "":
            # Confirma conexão
            pub(client_id+"/conectar/resposta", client_id)
            # Grava id do app
            aquario.appIdWrite(remetente)
            # Remove horario do arquivo indicando que a conexão foi estabelecida
            connBtn.removerHorario()
            # Atualiza variavel do identificador do app vinculado ao aquário
            app_id = remetente
    # So aceita mensagens do app vinculado
    elif app_id != "" and remetente == app_id:
        # Topico para bomba (Relé)
        if topico == (self.infoAquario.appId+"/atuadores/bomba"):
            if msg == "ligar":
                bomba.ligar()
            elif msg == "desligar":
                bomba.desligar()
        
        # Topico iluminação (Fita de Led)
        elif topico == (self.infoAquario.appId+"/atuadores/iluminacao"):
            cor = json.loads(msg)
            if cor["MODO"] == "cor":
                thrIlumState(cor["MODO"],cor["R"],cor["G"],cor["B"])
               
            elif cor["MODO"] == "especial":
                thrIlumState(cor["MODO"],cor["TIPO"])
                       
        # Topico alimentação
        elif topico == (self.infoAquario.appId+"/atuadores/alimentacao"):
            if payload == "P":
                alimentacao.alimentar(1)
               
            elif payload == "M":
                alimentacao.alimentar(2)
               
            elif payload == "G":
                alimentacao.alimentar(3)
        
def iniciar():
    global client_id
    global app_id
    global connected_flag
    # Variaveis de Conexão
    broker_address = "44.227.11.98"
    broker_port = 1883
    #usuario = ""
    #senha = ""

    # Cria uma nova instancia sem sessão limpa
    client = mqtt.Client(client_id,False)
    # Credenciais de acesso
    #client.username_pw_set(username=usuario,password=senha) 
    # Ativa logs do CLiente
    if mqttclient_log:
        client.on_log=on_log
        
    # Callback conexão
    client.on_connect = on_connect
       
    # Callback desconexão
    client.on_disconnect = on_disconnect
    # Callback de mensagens
    client.on_message = on_message
    # Inicia o loop em uma nova Thread 
    client.loop_start()
    # Conecta ao Broker
    client.connect(broker_address,broker_port)
    # Loop que aguarda a conexão
    while not client.connected_flag:
        print("Aguardando Conexão")
        time.sleep(5)
    return True

def parar():
    global thrIlum
    client.loop_stop()
    client.disconnect()
    if thrIlum.is_alive():
        print("matando thread")
        thrIlum.stop()

def sub(topico):
    global connected_flag
    if client.connected_flag:
        client.subscribe(topico,1)
    else:
        print("Falha de publicação: Sem conexão")

def pub (topico, msg):
    global connected_flag
    if client.connected_flag:
        payload={"SAID":client_id,
                 "MSG":msg
                 }
        client.publish(topico,json.dumps(payload))
    else:
        print("Falha de publicação: Sem conexão")
# Cria uma flag de conexão
mqtt.Client.connected_flag=False
# Cria uma flag de desconexão
mqtt.Client.disconnect_flag=False
# -- Ativa logs
mqttclient_log = False

# Identificadores
client_id = self.infoAquario.appId
app_id = aquario.appId()


