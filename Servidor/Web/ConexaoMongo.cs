using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using MongoDB.Driver;


namespace Web
{
    public class ConexaoMongo
    {
        public static string strcnn { get; set; }
        public MongoDB.Driver.MongoClient Conexao { get; set; }
        public ConexaoMongo()
        {
            Conexao = new MongoClient(strcnn);
        }

    }
}
