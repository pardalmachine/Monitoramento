var mysql = require('mysql');
var connection = mysql.createPool({
    host: '192.168.1.202',
    user: 'usrMonitora',
    password: 'Monitora',
    database: 'Monitora'
});
module.exports = connection;