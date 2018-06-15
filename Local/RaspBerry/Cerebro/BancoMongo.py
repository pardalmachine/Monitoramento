import datetime
import time
import json
from pymongo import MongoClient

class BancoMongo:
    client = ""
    base = ""

    def __init__(self):
        self.client =  MongoClient('mongodb://192.168.1.202:27017')
        #self.client = Connection()
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
            #insert["Hora"]="ISODate('"+datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')+"')"
            #insert["Hora"]="new Date()"
            insert["Hora"]=datetime.datetime.now()
            id = colecao.insert_one(insert).inserted_id
            print(id)