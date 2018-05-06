var express = require('express');
var ThemeParks = require('themeparks');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
    var disneyMagicKingdom = new ThemeParks.Parks.UniversalIslandsOfAdventure();

    // access wait times by Promise
    disneyMagicKingdom.GetWaitTimes().then(function(rides) {
        // print each wait time
        for(var i=0, ride; ride=rides[i++];) {
            console.log(ride.name + ": " + ride.waitTime + " minutes wait");
        }
    }, console.error);
});

module.exports = router;
