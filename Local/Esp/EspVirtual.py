import paho.mqtt.client as mqtt
import time
import json


class main:

    MeuNome=""
    Configuracao={}
    MeuNome="Esp1"
    Portas={}
    ConfiguracaoPorta={}

    def ConfiguraPortas(self, mensagem):
        Mensagem= mensagem.replace("'","\"")
        Configuracao=json.loads(Mensagem)
        print("Inicio de configuracao")
        print(Configuracao)
        
        for Sensor in Configuracao["Sensores"]:
            Portas[Sensor["Porta"]]="Porta "
            ConfiguracaoPorta[Sensor["Porta"]]=Sensor
            
        print(ConfiguracaoPorta)

    def on_connect(self, client, userdata, flags, rd):
        self.client.subscribe(self.MeuNome+"/#")
        self.client.publish('configuracao',MeuNome)
        time.sleep(2)
        self.client.publish('configuracao',self.MeuNome)


    def on_message(self, client, userdata, msg):
        #print(msg.topic + " " + str(msg.payload))

        Topicos = msg.topic.split("/")
        Mensagem = str(msg.payload.decode("utf-8"))
        if (len(Topicos)>=2):
            Acao=Topicos[1]
            print(Acao)
            if (Acao=="configuracao"):
                self.ConfiguraPortas(Mensagem)

    def Start(self)
        self.MeuNome="Esp1"
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect("192.168.1.201", 1883, 60)
        self.client.loop_start()
        ct=0
        while True:
            ct = ct + 1
            print(ct)
            time.sleep(1)
        self.client.loop_stop()