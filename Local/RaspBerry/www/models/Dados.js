var db = require('../dbConnection');
var moment = require('moment');

var Dados = {
    Sistemas: function (callback) {
        return db.query('select * from Sistema', callback)
    },

    Modulos: function (sistema, callback) {

        return db.query('select * from Modulo where Id_Sistema=? order by Nome', [sistema], callback);
    },

    Unidades: function (modulo, callback) {
        var sql = `
        select 
            Id_Modulo
            , Unidade
            , count(1) as Leituras
            , min(Hora) as Inicio, max(Hora) as Termino 
            from Valores 
            where Id_Modulo=? 
            GROUP BY Id_Modulo, Unidade
            order by Unidade;
            `;
        return db.query(sql, [modulo], callback);
    },

    Valores: function (modulo, unidade, de, ate, callback) {
        var De = moment(de.substring(0, 10));
        var Ate = moment(ate.substring(0, 10)).add('day', 1);
         console.log(De.format("YYYY-MM-DD HH:mm:ss"));
         console.log(Ate.format("YYYY-MM-DD HH:mm:ss"));

        return db.query(`
        select 
        avg(Valor) as Valor, convert((min(Hora) div 500)*500 , datetime) as Hora
        from Valores 
        where Id_Modulo=? and Unidade=? and Hora between ? and ?
        group by Hora div 500
        order by Hora;`, [
                modulo,
                unidade,
                De.format("YYYY-MM-DD HH:mm:ss"),
                Ate.format("YYYY-MM-DD HH:mm:ss")
            ], callback);
    }

};

module.exports = Dados;