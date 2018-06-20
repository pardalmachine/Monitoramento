import time
from Configuracao import Configuracao
from BancoMysql import BancoMysql
import paho.mqtt.client as mqtt

Conf = Configuracao()
Banco = BancoMysql()

Banco.VerificaSistema()

def on_connect(client, userdata, flags, rc):
    print("connectado no mqtt código" + str(rc))
    client.subscribe("#")


def on_message(client, userdata, msg):
    Mensagem = str(msg.payload.decode("utf-8"))
    print(Mensagem)
    print(msg.topic)
    if msg.topic == "configuracao":
        Conf.EnviaConfiguracao(client, Mensagem)
    if msg.topic == "valores":
        print("If Valores")
        Banco.GravaValores(Mensagem)

client = mqtt.Client("ConfigServer")
client.connect("192.168.1.201", 1883, 60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_start()

#conf = Configuracao()
while True:
    print("Servidor ...")
    time.sleep(1)
