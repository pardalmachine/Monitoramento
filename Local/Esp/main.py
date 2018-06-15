from umqtt.simple import MQTTClient
import json
import time
import machine
import random
class main:
    MeuNome=""
    Intervalo=1
    Sensores={}
    random.seed(12)
    Configuracao=False

    def Start(self):
        self.MeuNome="Esp1"
        self.Configuracao=False
        print("Entrei no Start")
        self.client=MQTTClient("Esp1","192.168.1.202")
        self.client.set_callback(self.on_message)
        self.client.connect()
        self.client.subscribe(self.MeuNome+"/#")
        time.sleep(2)
        self.client.publish('configuracao',self.MeuNome)
        ct=0
        while True:
            self.client.check_msg()

            time.sleep(1)
            if (ct>=self.Intervalo and self.Configuracao):
                ct=0
                self.LeValores()
                print("Realiza Leitura")
            ct+=1
        
    def on_message(self, topic, msg):
        Mensagem = str(msg.decode("utf-8"))
        Mensagem = Mensagem.replace("'","\"")
        strTopic = str(topic.decode("utf-8"))
        Topicos = strTopic.split("/")
        print(Mensagem)
        print(strTopic)
        
        if (len(Topicos)>=2):
            Acao=Topicos[1]
            if (Acao=="configuracao"):
                self.Sensores=json.loads(Mensagem)
                self.ConfiguraPortas()
        
    def ConfiguraPortas(self):
        print("Entrei na Configuracao")            
        self.Configuracao=True
        self.Intervalo=self.Sensores["Intervalo"]

    def LeValores(self):
        print("Inicio leitura de valores")
        retorno={}
        retorno["Leituras"]=[]
        for sensor in self.Sensores["Sensores"]:
            jValor={}
            jValor["Modulo"]=sensor["Modulo"]
            jValor["Id_Modulo"]=sensor["Id_Modulo"]
            jValor["Medicao"]=sensor["Medicao"]
            if sensor["Tipo"]=="ADC":
                valor=self.Map( random.randint(0,4095),0,4095,0,100)
                jValor["Valor"]=valor
            retorno["Leituras"].append(jValor)

        print(retorno)
        self.client.publish('valores',str(retorno))


    def Map(self, x, in_min, in_max, out_min, out_max):
        return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min

