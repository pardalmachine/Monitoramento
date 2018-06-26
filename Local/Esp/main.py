from umqtt.simple import MQTTClient
import json
import time
import machine
import random
import dht

class main:
    MeuNome=""
    Intervalo=10
    #Sensores={}
    random.seed(12)
    Configuracao=False
    Portas={}
    PortasConfig={}
    PortasLeitura={}
    SimulaLeitura=True

    def Start(self):
        self.MeuNome="Esp1"
        self.Configuracao=False
        #print("Entrei no Start")
        self.client=MQTTClient(self.MeuNome,"192.168.1.202")
        self.client.set_callback(self.on_message)
        self.client.connect()
        self.client.subscribe(self.MeuNome+"/#")
        time.sleep(2)
        self.client.publish('configuracao',self.MeuNome)
        ct=0
        while True:
            self.client.check_msg()
            if (self.Configuracao):
                ct+=1
                self.LeValores()
            if ct >= self.Intervalo:
                self.EnviaValores()
                ct=0

            time.sleep(1)
        
    def on_message(self, topic, msg):
        Mensagem = str(msg.decode("utf-8"))
        strTopic = str(topic.decode("utf-8"))
        Topicos = strTopic.split("/")
        print(Mensagem)
        print(strTopic)
        
        if (len(Topicos)>=2):
            Acao=Topicos[1]
            if (Acao=="configuracao"):
                self.ConfiguraPortas(Mensagem)
                #self.Sensores=json.loads(Mensagem)
                
        
    def ConfiguraPortas(self, mensagem):
        #print("Entrei na Configuracao")            
        mensagem = mensagem.replace("'","\"")
        config = json.loads(mensagem)
        self.Intervalo = config["Intervalo"]
        
        for confPorta in config["Sensores"]:
            numPorta = confPorta["Porta"]
            self.PortasConfig[numPorta]=confPorta
            self.PortasLeitura[numPorta]=0
            if (confPorta["Tipo"]=="ADC"):
                self.Portas[numPorta]=machine.ADC(machine.Pin(numPorta))
                
                if confPorta["Voltagem"]==3.6:
                    self.Portas[numPorta].atten(self.Portas[numPorta].ATTN_11DB)
                if confPorta["Voltagem"]==2:
                    self.Portas[numPorta].atten(self.Portas[numPorta].ADC_ATTEN_6db)
                if confPorta["Voltagem"]==1.34:
                    self.Portas[numPorta].atten(self.Portas[numPorta].ADC_ATTEN_2_5db)
                if confPorta["Voltagem"]==1:
                    self.Portas[numPorta].atten(self.Portas[numPorta].ADC_ATTEN_0db)

                if confPorta["bits"]==12:
                    self.Portas[numPorta].width(self.Portas[numPorta].WIDTH_12BIT)
                if confPorta["bits"]==11:
                    self.Portas[numPorta].width(self.Portas[numPorta].WIDTH_11BIT)
                if confPorta["bits"]==10:
                    self.Portas[numPorta].width(self.Portas[numPorta].WIDTH_10BIT)
                if confPorta["bits"]==9:
                    self.Portas[numPorta].width(self.Portas[numPorta].WIDTH_9BIT)
            if (confPorta["Tipo"]=="DHT"):
                #print(str(numPorta)+" na linha 84")
                #print (numPorta+100)
                #self.PortasLeitura[numPorta]=0
                self.PortasLeitura[numPorta+0.1]=0
                #print(confPorta)
                if confPorta["Modelo"]=="22":
                    self.Portas[numPorta]=dht.DHT22(machine.Pin(numPorta))
                if confPorta["Modelo"]=="11":
                    self.Portas[numPorta]=dht.DHT11(machine.Pin(numPorta))
        self.Configuracao=True
        #self.Intervalo=self.Sensores["Intervalo"]

    def LeValores(self):
        print("Inicio leitura de valores")
        for porta, pino in self.Portas.items():
            if self.PortasConfig[porta]["Tipo"]=="ADC":
                valor = pino.read()
                print("Original="+str(valor))
                if self.PortasConfig[porta]["Funcao"]=="Map":
                    valor = self.Map(valor, self.PortasConfig[porta]["InicioIni"],self.PortasConfig[porta]["InicioFim"],self.PortasConfig[porta]["FinalIni"],self.PortasConfig[porta]["FinalFim"])
                    print("Convertido="+str(valor))
                self.PortasLeitura[porta]+=valor
            if self.PortasConfig[porta]["Tipo"]=="DHT":
                #print('Leitura dht')
                pino.measure()
                self.PortasLeitura[porta]+=pino.temperature()
                self.PortasLeitura[porta+0.1]+=pino.humidity()
                #print (self.PortasLeitura[porta])
                #print (self.PortasLeitura[porta+0.1])
            

    def EnviaValores(self):
        #print("Envia Valores")
        retorno={}
        retorno["Leituras"]=[]
        for porta, pino in self.Portas.items():
            if self.PortasConfig[porta]["Tipo"]=="DHT":
                temperatura = self.PortasLeitura[porta]/self.Intervalo
                humidade = self.PortasLeitura[porta+0.1]/self.Intervalo
                self.PortasLeitura[porta]=0
                self.PortasLeitura[porta+0.1]=0

                jTemperatura={}
                jTemperatura["Id_Modulo"]=self.PortasConfig[porta]["Id_Modulo"]
                jTemperatura["Medicao"]="Temperatura"
                jTemperatura["Valor"]=temperatura
                retorno["Leituras"].append(jTemperatura)


                jHumidade={}
                jHumidade["Id_Modulo"]=self.PortasConfig[porta]["Id_Modulo"]
                jHumidade["Medicao"]="Humidade"
                jHumidade["Valor"]=humidade
                retorno["Leituras"].append(jHumidade)


                #print('entrei no dht')
            else:
                valor = self.PortasLeitura[porta]
                self.PortasLeitura[porta]=0
                jValor={}
                jValor["Id_Modulo"]=self.PortasConfig[porta]["Id_Modulo"]
                jValor["Medicao"]=self.PortasConfig[porta]["Medicao"]
                if self.PortasConfig[porta]["Acumulo"]=="Media":
                    valor=valor/self.Intervalo
                jValor["Valor"]=valor
                retorno["Leituras"].append(jValor)
        self.client.publish('valores',str(retorno))



    def Map(self, x, in_min, in_max, out_min, out_max):
        return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min

