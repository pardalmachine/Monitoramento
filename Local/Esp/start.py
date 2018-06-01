import paho.mqtt.client as mqtt
import logging
import time
import json

#from Configuracao import Configuracao
#Config = Configuracao()
Sensores={}
MeuNome = "Esp1"
Intervalo=1
client = mqtt.Client(MeuNome)
client.connect('192.168.1.201',1883,60)


def on_connect(client, userdata, flags, rc):
    client.subscribe(MeuNome+"/#")
    client.publish('configuracao',MeuNome)

def on_message(client, userdata, msg):
    Mensagem = str(msg.payload.decode("utf-8"))
    Mensagem = Mensagem.replace("'","\"")
    Topico = msg.topic.split("/")
    if (len(Topico)>=2):
        Acao=Topico[1]
        if (Acao=="configuracao"):
            global Intervalo
            global Sensores
            Sensores=json.loads(Mensagem)
            Intervalo=Sensores["Intervalo"]
            ConfiguraPortas()

def ConfiguraPortas():
    for sensor in Sensores["Sensores"]:
        print(sensor)

client.on_connect = on_connect
client.on_message = on_message

client.loop_start()
while True:
    time.sleep(Intervalo)

client.disconnect()
