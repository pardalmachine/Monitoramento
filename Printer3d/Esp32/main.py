import gc
from umqtt.simple import MQTTClient
import json
import time
import machine
import math


class main:
    MeuNome = ""
    Intervalo = 10
    adc = machine.ADC(machine.Pin(35))
    Contator = machine.Pin(34, machine.Pin.IN)
    SemiVolta=0
    def trgContador(self, p):
        vlrPino=p.value()
        if (vlrPino!=self.SemiVolta):
            self.SemiVolta=vlrPino
            if (vlrPino==0):
                print('SemiVolta')
                retorno={}
                retorno["Leituras"]=[]
                envio={}
                envio["Id_Modulo"]=2
                envio["Medicao"]="SemiVolta"
                envio["Valor"]=1
                retorno["Leituras"].append(envio)
                self.client.publish('valores',str(retorno))



    def Start(self):
        gc.enable()
        self.MeuNome = "Prt3d"
        self.adc.atten(self.adc.ATTN_11DB)
        self.adc.width(self.adc.WIDTH_10BIT)

        #self.Contator.irq(trigger=machine.Pin.IRQ_RISING,
        #                  handler=self.trgContador)

        print("Entrei no start")
        self.client = MQTTClient(self.MeuNome, "192.168.1.203")
        self.client.set_callback(self.on_message)
        self.client.connect()
        self.client.subscribe(self.MeuNome+"/#")
        ct=0
        tMedia=0
        Pino=self.Contator.value()
        PinoAnterior=self.Contator.value()
        while True:
            tMedia+=self.LeTemperatura(self.adc.read())
            if ct>=9:
                tMedia=tMedia/ct
                print(tMedia)
                retorno={}
                retorno["Leituras"]=[]
                envio={}
                envio["Id_Modulo"]=2
                envio["Medicao"]="Temperatura"
                envio["Valor"]=tMedia
                retorno["Leituras"].append(envio)
                self.client.publish('valores',str(retorno))
                ct=0
                tMedia=0

            # print(self.Contator.value())
            time.sleep(0.5)
            Pino=self.Contator.value()
            if Pino!=PinoAnterior:
                PinoAnterior=Pino
                if Pino==0:
                    print('SemiVolta')
                    retorno={}
                    retorno["Leituras"]=[]
                    envio={}
                    envio["Id_Modulo"]=2
                    envio["Medicao"]="SemiVolta"
                    envio["Valor"]=1
                    retorno["Leituras"].append(envio)
                    self.client.publish('valores',str(retorno))

            ct+=1

    def on_message(self, topic, msg):
        Mensagem=str(msg.decode("utf-8"))
        strTopic=str(topic.decode("utf-8"))
        Topicos=strTopic.split("/")
        print(Mensagem)
        print(strTopic)

    def LeTemperatura(self, LeituraADC):
        R1=10000
        c1=1.009249522e-03
        c2=2.378405444e-04
        c3=2.019202697e-07
        R2=R1 * (1023.0 / LeituraADC - 1.0)
        logR2=math.log(R2)
        T=(1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2))
        Tc=T - 273.15
        return Tc

    def Map(self, x, in_min, in_max, out_min, out_max):
        return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min
