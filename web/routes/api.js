var express = require('express');
var router = express.Router();

var usersRouter = require('./users');
var waittimeRouter = require('./waittime');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.use('/users', usersRouter);
router.use('/waittime', waittimeRouter);

module.exports = router;
