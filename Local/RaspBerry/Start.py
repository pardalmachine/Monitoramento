import json
with open("Config.json") as data_file:
    config=json.load(data_file)

Placas=dict()

for modulo in config["Modulos"]:
    for sensor in modulo["Sensores"]:
        if Placas.__contains__(sensor["IdPlaca"])==False:
            Placas[sensor["IdPlaca"]]=dict()
        if  Placas[sensor["IdPlaca"]].__contains__(sensor["Porta"])==False:
            Placas[sensor["IdPlaca"]][sensor["Porta"]]=sensor["Tipo"]+","+ sensor["Medicao"]+",Sensor"

print(str(Placas["Esp1"]))
