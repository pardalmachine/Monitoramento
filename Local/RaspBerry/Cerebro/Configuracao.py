import json
from BancoMysql import BancoMysql

class Configuracao:
    def EnviaConfiguracao(self, client, destinatario):
        client.publish(destinatario + "/configuracao",
                       str(self.Configuracao(destinatario)))

    def Configuracao(self, Placa):
        banco = BancoMysql()
        with open("Config.json") as data_file:
            config = json.load(data_file)
        retorno = {}
        retorno["Intervalo"] = config["Intervalo"]
        retorno["Sensores"] = []
        for modulo in config["Modulos"]:
            for sensor in modulo["Sensores"]:
                if Placa == sensor["IdPlaca"]:
                    Id=banco.IdModulo(config["Sistema"], modulo["Nome"])
                    jPlaca = {}
                    jPlaca["Tipo"] = sensor["Tipo"]
                    jPlaca["Porta"] = sensor["Porta"]
                    jPlaca["Id_Modulo"] = Id
                    if sensor["Tipo"].__contains__("ADC") == True:
                        jPlaca["Voltagem"] = sensor["Voltagem"]
                        jPlaca["bits"] = sensor["bits"]
                        jPlaca["RangeIni"] = sensor["RangeIni"]
                        jPlaca["RangeFim"] = sensor["RangeFim"]
                        jPlaca["Modulo"] = modulo["Nome"]
                        jPlaca["Medicao"] = sensor["Medicao"]
                    retorno["Sensores"].append(jPlaca)
        banco.Dispose()
        return retorno
