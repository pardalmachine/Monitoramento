using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace Web.Dados
{
    public class ClMedicao
    {
        [BsonId()]
        public ObjectId Id { get; set; }
        [BsonElement("Medicao")]
        public string Medicao { get; set; }
        [BsonElement("Valor")]
        public decimal Valor { get; set; }
        [BsonElement("Hora")]
        public DateTime Hora { get; set; }
    }
}
