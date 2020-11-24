This is a WIP maybe to never be finished please understand :(

# TWITGEN
This is a useless random tweets dataset generator. Given some parameters and a .json file of twitter [places](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/overview/geo-objects#place) this python script will slowly generate a random dataset of a given number of tweets using Twitter API 1.1 format.

## Setup
For the main script twitgen.py the only requirement is Python3 and [shapely](https://pypi.org/project/Shapely/) (just 'pip install shapely' I guess?).
There is one more script which lets you collect the needed array of places (one test file is already provided though), getplaces.js. Just run 'npm install' and you should be alright, otherwise try 'npm install twitter-lite dotenv'.
### Setting up twitgen.py
The main python script has some parameters to fill (it has some default ones as an example).
**N_TWEETS** is obviously the number of tweets to be generated (beware the script is slow don't go too high)
**GEO_CHANCE** is the chance (between 0.0~1.0) of a tweet having a geolocation. Generating a random coordinate according to a given twitter place is the actual slow part of the script, beware of this amount.
**LOCATIONS_FILE** is the twitter places file. Every time a tweet should have a geolocation, one place at random from this json array will be chosen.
**HASHTAGS** array of ["tag", *chance*] pairs, each one of these has *chance* chance to appear in a given tweet. (So to be clear, all or none of those may appear in each tweet).
**TIME_RANGE** is a range array in the form ["start date", "end date"] of two dates in the "YEAR-MONTH-DAY" format. Every generated tweet is dated between this range. 

Once all of this is done you are ready to launch the script with 'python3 twitgen.py'.
When done the output json of tweets is saved in out_twitgen.json.

### Setting and launching getplaces.js
Bad news: you are gonna need a twitter dev account to access their API. Once you have your dev account data create a '.env' file in the main directory with your info in this format:

BEARER_TOKEN=''
CONSUMER_KEY=''
CONSUMER_SECRET=''
ACCESS_TOKEN_KEY=''
ACCESS_TOKEN_SECRET=''

Then launch the script with 'node getplaces.js output_path place_name [neighborhood/city/admin/country]', last parameter is optional but should be used to get a larger bounding box for the place as the default is neighborhood. When the output file does not exist it is created, else the script will append the new place to the list.

# WIP
adding images someday :(


