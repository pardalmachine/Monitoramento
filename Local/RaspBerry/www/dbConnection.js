var mysql = require('mysql');
var connection = mysql.createPool({
    host: '192.168.1.201',
    user: 'usrMonitora',
    password: '#Monitora547',
    database: 'Monitora'
});
module.exports = connection;