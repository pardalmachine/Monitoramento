using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Driver.Linq;
using Newtonsoft.Json.Linq;

namespace Web.Api
{
    [Route("api/[controller]")]
    [ApiController]
    public class MonitoramentoController : ControllerBase
    {
        [HttpGet("[action]")]
        public List<Dados.Bases> Bases()
        {
            var cn = new ConexaoMongo().Conexao;
            List<Dados.Bases> retorno = new List<Dados.Bases>();
            //List<MongoDB.Bson.BsonDocument> retorno = new List<BsonDocument>();
            //BsonArray retorno = new BsonArray();
            using (IAsyncCursor<BsonDocument> cursor = cn.ListDatabases())
            {
                while (cursor.MoveNext())
                {
                    foreach (var doc in cursor.Current)
                    {
                        Dados.Bases item = new Dados.Bases()
                        {
                            Nome = doc["name"].ToString(),
                            Tamanho = doc["sizeOnDisk"].ToInt32()

                        };
                        retorno.Add(item);
                    }

                }
            }
            return retorno;
        }

        [HttpGet("[action]/{nomebase}")]
        public List<string> Colecoes(string nomebase)
        {
            var cn = new ConexaoMongo().Conexao;
            List<string> retorno = new List<string>();
            var db = cn.GetDatabase(nomebase);
            //List<MongoDB.Bson.BsonDocument> retorno = new List<BsonDocument>();
            //BsonArray retorno = new BsonArray();

            using (IAsyncCursor<BsonDocument> cursor = db.ListCollections())
            {
                while (cursor.MoveNext())
                {
                    foreach (var doc in cursor.Current)
                    {
                        retorno.Add(doc["name"].ToString());
                    }

                }
            }
            return retorno;
        }

        [HttpGet("[action]/{nomebase}/{colecao}")]
        public JArray Medicoes(string nomebase, string colecao)
        {
            var cn = new ConexaoMongo().Conexao;
            var db = cn.GetDatabase(nomebase);
            var cl = db.GetCollection<Dados.ClMedicao>(colecao);
            var consulta = (from dados in cl.AsQueryable<Dados.ClMedicao>()
                            group dados by dados.Medicao into g
                            select new
                            {
                                Medicao=g.Key,
                                Inicio=g.Min(p=>p.Hora),
                                Termino=g.Max(p=>p.Hora),
                                Total=g.Count()
                            }).ToList();
            return JArray.FromObject(consulta);
        }

        [HttpPost("[action]")]
        public JArray MedicoesDias([FromBody] JObject prm)
        {
            var cn = new ConexaoMongo().Conexao;
            var db = cn.GetDatabase(prm["base"].ToString());
            var cl = db.GetCollection<Dados.ClMedicao>(prm["colecao"].ToString());
            string medicao = prm["medicao"].ToString();
            var pre = (from dados in cl.AsQueryable<Dados.ClMedicao>()
                            where dados.Medicao == medicao
                            select dados);

            List<DateTime> dias = new List<DateTime>();
            foreach(var dia in pre)
            {
                dias.Add(new DateTime(dia.Hora.Year, dia.Hora.Month, dia.Hora.Day));
            }
            var consulta = (from dados in dias
                            group dados by dados.Date into g
                            select new
                            {
                                Dia = g.Key,
                                Leituras = g.Count()
                            }).ToList();

            return JArray.FromObject(consulta);
        }


        [HttpPost("[action]")]
        public JArray MedicoesDiasValores([FromBody] JObject prm)
        {
            var cn = new ConexaoMongo().Conexao;
            var db = cn.GetDatabase(prm["base"].ToString());
            var cl = db.GetCollection<Dados.ClMedicao>(prm["colecao"].ToString());
            string medicao = prm["medicao"].ToString();
            DateTime inicio = prm["dia"].ToObject<DateTime>();
            DateTime fim = inicio.AddDays(1);
            List<Dados.ClMedicao> ListaTemp = new List<Dados.ClMedicao>();
            var pre = (from dados in cl.AsQueryable<Dados.ClMedicao>()
                       where 
                       dados.Medicao == medicao 
                       select dados).ToList();
            foreach (Dados.ClMedicao item in pre)
                ListaTemp.Add(item);

            return JArray.FromObject(ListaTemp.Where(p => (p.Hora >= inicio & p.Hora < fim)).OrderBy(p => p.Hora));
        }

    }
}