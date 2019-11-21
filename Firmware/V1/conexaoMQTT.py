# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 10:38:12 2019

@author: Daniel Araújo Chaves Souza
"""
# Imports
# -- importa biblioteca do eclipse paho
import paho.mqtt.client as mqtt
# -- importa informaçõe do aquario
import smartAquario as aquario
# -- importa controle do led conexão (Azul)
import connLed
# -- importa rotina do botao de reset
import connBtn
# -- importa controle da bomba
import bomba
# -- importa controle de iluminação
import iluminacao
# -- importa controle de alimentação
import alimentacao
# -- importa temporizador
import time

thrIlum = iluminacao.estado(0)

def thrIlumState(modo):
    global thrIlum
    # Para a thread se ela estiver executando
    if thrIlum.is_alive():
        print("matando thread")
        thrIlum.stop()
    # Inicia um nova thread com o novo estado
    thrIlum = iluminacao.estado(modo)
    thrIlum.start()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # Conexão bem sucedida
        client.connected_flag = True
        # Liga led de conexão
        connLed.ligar()
        print("Conexão Estabelecida")
    else:
        print("Errod de conexão=",rc)
        
def on_disconnect(client, userdata, rc):
    print("motivo da desconexão" + str (rc))
    connLed.desligar()
    client.connected_flag = False
    client.disconnect_flag = True
    
def on_log(client, userdata, level, buf):
   print(buf)
   
def on_message(client, userdata, message):
    # Objeto global da Thread de iluminação
    global thrIlum
    
    topico = message.topic
    payload = str(message.payload.decode("utf-8"))
    
    if topico == (aquario.id()+"/conectar"):
        if connBtn.connState():
            # Se o botao de conexão não foi pressionado a menos de 30s
            pub(client_id+"/conectar/resposta", "ERRO")
        elif payload != "":
            # Confirma conexão
            pub(client_id+"/conectar/resposta", client_id)
            # Grava id do app
            aquario.appIdWrite(payload)
            # Remove horario do arquivo indicando que a conexão foi estabelecida
            connBtn.removerHorario()
    # Topico para bomba (Relé)
    elif topico == (aquario.id()+"/atuadores/bomba"):
        if payload == "ligar":
            bomba.ligar()
        elif payload == "desligar":
            bomba.desligar()
    
    # Topico iluminação (Fita de Led)
    elif topico == (aquario.id()+"/atuadores/iluminacao"):
        if payload == "azul":
            thrIlumState(1)
           
        elif payload == "vermelho":
            thrIlumState(2)
           
        elif payload == "verde":
            thrIlumState(3)
           
        elif payload == "especial1":
            thrIlumState(4)
           
        elif payload == "desligar":
            thrIlumState(0)
    
    # Topico alimentação
    elif topico == (aquario.id()+"/atuadores/alimentacao"):
        if payload == "P":
            alimentacao.alimentar(1)
           
        elif payload == "M":
            alimentacao.alimentar(2)
           
        elif payload == "G":
            alimentacao.alimentar(3)
        
def iniciar():
    client.loop_start()
    # Conecta ao Broker
    client.connect(broker_address,broker_port)
    # Loop que aguarda a conexão
    while not client.connected_flag:
        print("Aguardando Conexão")
        time.sleep(5)
    return True

def parar():
    client.loop_stop()
    client.disconnect()
    if thrIlum.is_alive():
        print("matando thread")
        thrIlum.stop()

def sub(topico):
    if client.connected_flag:
        client.subscribe(topico,1)
    else:
        print("Falha de publicação: Sem conexão")

def pub (topico, msg):
    if client.connected_flag:
        client.publish(topico,msg)
    else:
        print("Falha de publicação: Sem conexão")
# Cria uma flag de conexão
mqtt.Client.connected_flag=False
# Cria uma flag de desconexão
mqtt.Client.disconnect_flag=False
# -- Ativa logs
mqttclient_log = False

# Variaveis de Conexão
broker_address = "localhost"
broker_port = 1883
client_id = aquario.id()
usuario = ""
senha = ""

# Cria uma nova instancia sem sessão limpa
client = mqtt.Client(client_id,False)
# Credenciais de acesso
#client.username_pw_set(username=usuario,password=senha) 
# Ativa logs do CLiente
if mqttclient_log:
    client.on_log=on_log
# Callback conexão
try:
    client.on_connect = on_connect
except:
    print("Falha na conexão")
    exit(1)
    
# Callback desconexão
client.on_disconnect = on_disconnect
# Callback de mensagens
client.on_message = on_message
# Inicia o loop em uma nova Thread 