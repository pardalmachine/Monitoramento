var express = require('express');
var router = express.Router();
var db = require('../db')

/* GET ALL BOOKS */
router.get('/', function (res, next) {
  res.json({ abc: '123' });
});

router.post('/valores', function (req, res, next) {
  var base = db.get().db(req.body.base);
  var colecao = base.collection(req.body.colecao);
  var medicao = req.body.medicao;
  var de = new Date(req.body.de);
  var ate = new Date(req.body.ate);
  ate.setDate(ate.getDate() + 1);
  //var de = new Date("2018-06-09T00:00:00.000Z");
  console.log(de);
  console.log(ate);
  //var ate = new Date("2018-06-10T00:00:00.000Z");
  // "Hora": { $gte: "2018-06-09T00:00:00Z" }
  //    "Medicao": medicao,
  // "Valor": { $gt: 22.1978 }

  var consulta = {
    "Medicao": medicao,
    "Hora": { $gte: de, $lte: ate }
  };

  console.log(consulta);
  colecao.find(consulta).toArray(function (err, result) {
    if (err) {
      console.log(err);
    }
    else {
      console.log(result.length);
    }


    res.json(result);
  });

});


router.post('/medicao', function (req, res, next) {
  var base = db.get().db(req.body.base);
  var colecao = base.collection(req.body.colecao);
  // console.log(req.body.base);
  // console.log(req.body.colecao);
  var cursor = colecao.aggregate(
    [
      {
        $group: {
          _id: '$Medicao',
          De: { $min: "$Hora" },
          Ate: { $max: "$Hora" },
          Leituras: { $sum: 1 }

        }
      }
    ],
    { cursor: { batchSize: 100 } }
  );
  cursor.get(function (err, results) {
    // console.log('entrei no cursor');
    // console.log(results);
    res.json(results);
  });
});



router.post('/collections', function (req, res, next) {
  var base = db.get().db(req.body.base);
  res.set('Content-Type', 'application/json');
  base.listCollections().toArray(function (err, item) {
    console.log(item);
    res.send(item);
    //res.json(item);
  });
});


router.get('/databases', function (req, res, next) {
  res.set('Content-Type', 'application/json');
  var adminDb = db.get().db('admin').admin();
  adminDb.listDatabases(function (err, dbs) {
    //res.send(dbs.databases.filter(p => p.name != 'admin' && p.name != 'config' && p.name != 'local'));
    res.send(201, [{ "name": "PlacaSolar", "sizeOnDisk": 143360, "empty": false }, { "name": "basex", "sizeOnDisk": 32768, "empty": false }])
  });

});

module.exports = router;