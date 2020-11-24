/*Script to manually gather Twitter Places via their 1.1 API*/
/*Each call to the same file will append the new place*/

const Twitter = require('twitter-lite');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const BEARER_TOKEN = process.env.BEARER_TOKEN;
const CONSUMER_KEY = process.env.CONSUMER_KEY;
const CONSUMER_SECRET = process.env.CONSUMER_SECRET;
const ACCESS_TOKEN_KEY = process.env.ACCESS_TOKEN_KEY;
const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET;

const app = new Twitter({
    bearer_token: BEARER_TOKEN
});

const usr = new Twitter({
    consumer_key: CONSUMER_KEY,
    consumer_secret: CONSUMER_SECRET,
    access_token_key: ACCESS_TOKEN_KEY,
    access_token_secret: ACCESS_TOKEN_SECRET
});

if(process.argv.length < 4){
    console.log("Usage: ./program filename location [neighborhood/city/admin/country]")
    return
}

var jfile = process.argv[2]

var place = process.argv[3];
//granularity is either neighborhood,city,admin or country
//default is neighborhood
var granularity = process.argv[4];

var params = {
    "query": place,
}

if(granularity) params["granularity"] = granularity;

usr.get('geo/search', params).then((res) => {
    let newplace = res.result.places[0];
    try {
        let data = fs.readFileSync(path.join(__dirname, "/" + jfile));
        places = JSON.parse(data);
        places.push(newplace);
        data = JSON.stringify(places, null, 2);
        fs.writeFileSync(path.join(__dirname, "/" + jfile), data);
    } catch(err) {
        console.log(err);
        let list = [newplace];
        let data = JSON.stringify(list, null, 2);
        fs.writeFileSync(path.join(__dirname, "/" + jfile), data);
    }
    console.log(JSON.stringify(newplace, null, 2));
}).catch((err) => { console.log(err); });
