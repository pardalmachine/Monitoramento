var express = require('express');
var router = express.Router();
var Dados = require('../models/Dados');

router.get('/sistemas', function (req, res, next) {
    Dados.Sistemas(function (err, rows) {
        if (err) res.json(err);
        else {
            res.json(rows)
        }
    });
});

router.get('/modulos/:id', function (req, res, next) {

    Dados.Modulos(req.params.id, function (err, rows) {
        if (err) res.json(err)
        else {
            res.json(rows);
        }
    });
});


router.get('/unidades/:id', function (req, res, next) {

    Dados.Unidades(req.params.id, function (err, rows) {
        if (err) res.json(err)
        else {
            res.json(rows);
        }
    });
});

router.post('/valores', function (req, res, next) {

    Dados.Valores(
        req.body.modulo
        , req.body.unidade
        , req.body.de
        , req.body.ate, function (err, rows) {
            if (err) {
                res.json(err)
            }
            else {
                res.json(rows);
            }
        });
});

module.exports = router;