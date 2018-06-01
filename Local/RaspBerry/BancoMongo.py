from pymongo import MongoClient
import datetime
import time
import json


class BancoMongo:
    client = ""
    base = ""

    def __init__(self):
        self.client = MongoClient('192.168.1.201', 27017)
        self.base = self.client['PlacaSolar']

    #clValores = base["Valores"]

    def GravaValor(self, registro):
        print("Grava")
        valores = json.loads(registro.replace("'", "\""))
        for valor in valores["Leituras"]:
            print(valor)
            colecao = self.base[valor["Modulo"]]
            insert = {}
            insert["Medicao"] = valor["Medicao"]
            insert["Valor"] = valor["Valor"]
            insert["Hora"]=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            id = colecao.insert_one(insert).inserted_id
            print(id)