import json

class Configuracao:
    def EnviaConfiguracao(self, client, destinatario):
        print("Entrei na funcao")
        client.publish(destinatario+"/configuracao",str(self.Configuracao(destinatario)))



    def Configuracao(self, Placa):
        with open("Config.json") as data_file:
            config=json.load(data_file)
        retorno = {}
        retorno["Intervalo"]=config["Intervalo"]
        retorno["Sensores"]=[]
        for modulo in config["Modulos"]:
            for sensor in modulo["Sensores"]:
                if (Placa.__contains__(sensor["IdPlaca"]))==True:
                    jPlaca={}
                    jPlaca["Tipo"]=sensor["Tipo"]
                    jPlaca["Porta"]=sensor["Porta"]
                    if sensor["Tipo"].__contains__("ADC")==True:
                        jPlaca["Voltagem"]=sensor["Voltagem"]
                        jPlaca["bits"]=sensor["bits"]
                        jPlaca["RangeIni"]=sensor["RangeIni"]
                        jPlaca["RangeFim"]=sensor["RangeFim"]
                        jPlaca["Modulo"]=modulo["Nome"]
                    retorno["Sensores"].append(jPlaca)
        
        return retorno
