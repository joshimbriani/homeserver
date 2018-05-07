var express = require('express');
var ThemeParks = require('themeparks');
var fs = require("fs");
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
    var rides = [];
    const favs = JSON.parse(fs.readFileSync('./config/waittime.json'))["rides"];
    
    var ioa = new ThemeParks.Parks.UniversalIslandsOfAdventure();
    var usf = new ThemeParks.Parks.UniversalStudiosFlorida();

    // access wait times by Promise
    ioa.GetWaitTimes().then(function(ioaRides) {

        usf.GetWaitTimes().then(function(usfRides) {
            var rides = ioaRides.concat(usfRides);
            rides = rides.map(r => rideToObject(r));

            var returnRides = [];

            for (var i = 0; i < favs.length; i++) {
                returnRides.push(search(favs[i], rides));
            }

            res.send(JSON.stringify(returnRides)); 
        })

    }, console.error);
});

/* GET users listing. */
router.get('/all', function(req, res, next) {
    var rides = [];
    var ioa = new ThemeParks.Parks.UniversalIslandsOfAdventure();
    var usf = new ThemeParks.Parks.UniversalStudiosFlorida();

    // access wait times by Promise
    ioa.GetWaitTimes().then(function(ioaRides) {

        usf.GetWaitTimes().then(function(usfRides) {
            var rides = ioaRides.concat(usfRides);
            rides = rides.map(r => rideToObject(r));

            res.send(JSON.stringify(rides)) 
        })

    }, console.error);
});

function rideToObject(r) {
    return {"name": r.name, 'waitTime': r.waitTime};
}

function search(nameKey, myArray){
    for (var i=0; i < myArray.length; i++) {
        if (myArray[i].name === nameKey) {
            return myArray[i];
        }
    }
}


module.exports = router;
