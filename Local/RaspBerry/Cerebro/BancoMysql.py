import mysql.connector as MariaDB
import json


class BancoMysql:
    Sistema=""
    Id_Sistema=0
    def __init__(self):
        self.cliente = MariaDB.connect(
            user='root',
            password='Mercado1',
            host='192.168.1.202',
            database='Monitora')
    
    def Dispose(self):
        self.cliente.close()
        print("conexao fechada")

    def VerificaSistema(self):
        with open("Config.json") as data_file:
            config = json.load(data_file)

        self.Sistema = config["Sistema"]
        print("Inicio da verficacao")
        cursor = self.cliente.cursor(buffered=True)
        consulta = ("select Id, Nome from Sistema where Nome=%s")
        cursor.execute(consulta, (self.Sistema, ))
        if cursor.rowcount <= 0:
            print(self.Sistema)
            sql = "INSERT INTO Sistema(Nome)  VALUES (%s)"
            cursor.execute(sql, (config["Sistema"], ))
            self.cliente.commit()
            cursor.execute(consulta, (self.Sistema, ))

        
        for (Id, Nome) in cursor:
            self.Id_Sistema = Id

        for modulo in config["Modulos"]:
            Nome = str(modulo["Nome"])
            consulta = (
                "SELECT Id, Id_Sistema Nome from Modulo WHERE Nome = %s and Id_Sistema=%s "
            )
            cursor.execute(consulta, (Nome, self.Id_Sistema))
            if cursor.rowcount <= 0:
                print("Novo modulo")
                sql = "INSERT INTO Modulo(Nome, Id_Sistema)  VALUES ( %s , %s )"
                cursor.execute(sql, (Nome, self.Id_Sistema))
                self.cliente.commit()

    def IdModulo(self, sistema, modulo):
        retorno = 0
        cursor = self.cliente.cursor(buffered=True)
        consulta = ("select Modulo.Id from Sistema inner join Modulo on Sistema.Id = Modulo.Id_Sistema where Sistema.Nome=%s and Modulo.Nome=%s;")
        cursor.execute(consulta,(sistema, modulo))
        if cursor.rowcount>0:
            id = cursor.fetchone()
            print(id[0])
            return id[0]
        return retorno

    
    def GravaValores(self, msg):
        Mensagem = msg.replace("'","\"")
        leituras = json.loads(Mensagem)
        cursor = self.cliente.cursor(buffered=True)
        for leitura in leituras["Leituras"]:
            insert = ("insert into Valores (Id_Modulo, Unidade, Valor) values (%s,%s,%s)")
            cursor.execute(insert,(leitura["Id_Modulo"], leitura["Medicao"], leitura["Valor"]))
        self.cliente.commit()
        #for(medicao in leituras["Leituras"]):
    

