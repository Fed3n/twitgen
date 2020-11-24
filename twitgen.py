import json
import datetime
import time
import copy
import random
from shapely.geometry import Polygon, Point

##SETTINGS##
N_TWEETS = 100 
#CHANCE OF TWEETS WITH COMPLETE GEO (be careful geo can be very slow to process especially with large bounding boxes)
GEO_CHANCE = 0.4
#JSON FILE OF TWITTER'S 'PLACE' ARRAY [from where a random location will be equally chosen]
LOCATIONS_FILE = "citta_italia.json"
#ONE OR MORE HASHTAG PER TWEET [number is chance of each]
HASHTAGS = [["covid",0.6], ["lockdown",0.4],["vaccino",0.2],["2021",0.3]]
TIME_RANGE = ["2020-10-01", "2020-12-31"]
###########

#CONSTS
TWID_BASE = 1000000000000000000
TWID_MAX = 1999999999999999999
UID_BASE = 100000000
UID_MAX = 999999999


###TEMPLATES###
TWEET = {
    "created_at": "",
    "id": None,
    "id_str": "",
    "text": "",
    "truncated": False,
    "entities": {
        "hashtag": [],
        "symbols": [],
        "user_mentions": [],
        "urls": [],
    },
    "metadata": {
        "iso_language_code": "en",
        "result_type": "recent"
    },
    "source": "",
    "in_reply_to_status_id": None,
    "in_reply_to_status_id_str": None,
    "in_reply_to_user_id": None,
    "in_reply_to_user_id_str": None,
    "in_reply_to_screen_name": None,
    "user": {
        "id": None,
        "id_str": "",
        "screen_name": ""
    },
    "geo": None,
    "coordinates": None,
    "place": None,
    "contributors": None,
    "is_quote_status": False,
    "retweet_count": 0,
    "favorited": False,
    "retweeted": False,
    "lang": "en"
}

GEO = {
    "type": "Point",
    "coordinates": {
        "0": None,
        "1": None
    }
}

COORDINATES = {
    "type": "Point",
    "coordinates": {
        "0": None,
        "1": None
    }
}
##############

def get_random_date(daterange):
    start = time.mktime(time.strptime(daterange[0], "%Y-%m-%d"))
    end = time.mktime(time.strptime(daterange[1], "%Y-%m-%d"))
    rngtime = start + (random.random()*(end-start))
    return time.strftime("%a %b %d %H:%M:%S %z %Y", time.localtime(rngtime))
    

def parse_locations():
    with open(LOCATIONS_FILE) as f:
        data = f.read()
        places = json.loads(data)
        return places

def get_random_points(bbox, n):
    poly = Polygon([(bbox[0][0],bbox[0][1]),(bbox[1][0],bbox[1][1]),(bbox[2][0],bbox[2][1]),(bbox[3][0],bbox[3][1]),(bbox[4][0],bbox[4][1])])
    minx, maxx, miny, maxy = poly.bounds
    points = []
    while len(points) < n:
        rng_point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if(rng_point.within(poly)):
            points.append(rng_point)
    return points

def main():
    tweetlist = []
    places = parse_locations()
    #points = get_random_points(places[0]["bounding_box"]["coordinates"][0],3)
    for i in range(N_TWEETS):
        #progress countup :')))) you are gonna need it for sanity
        print(f"{i+1} tweets generated", end=("\n" if (i+1)>=N_TWEETS else "\r"))
        tweet = copy.deepcopy(TWEET)
        twid = TWID_BASE + random.random() * (TWID_MAX - TWID_BASE)
        uid = UID_BASE + random.random() * (UID_MAX - UID_BASE)

        tweet["id"] = twid
        tweet["id_str"] = f"{int(twid)}"

        tweet["created_at"] = get_random_date(TIME_RANGE)
        
        tweet["user"]["id"] = uid
        tweet["user"]["id_str"] = f"{int(uid)}"
        tweet["user"]["name"] = f"user{int(uid)}"
        tweet["user"]["screen_name"] = f"user{int(uid)}"
        
        #Setting geoinfo for some tweets this might be very slow tbh
        if random.random() <= GEO_CHANCE:
            tweet["place"] = random.choice(places)
            point = get_random_points(tweet["place"]["bounding_box"]["coordinates"][0],1)[0]
            
            tweet["geo"] = copy.deepcopy(GEO)
            tweet["geo"]["coordinates"]["0"] = point.y
            tweet["geo"]["coordinates"]["1"] = point.x

            tweet["coordinates"] = copy.deepcopy(COORDINATES)
            tweet["coordinates"]["coordinates"]["0"] = point.x
            tweet["coordinates"]["coordinates"]["1"] = point.y
        
        ##GENERATING TEXT MESSAGE AND ENTITIES
        #hashtags
        hashlist = []
        for tag in HASHTAGS:
            if random.random() <= tag[1]:
                hashlist.append(tag[0])
        
        #tweet text and appending entities
        #every entity in a tweet has indices which identify at what point of the text it occurs
        tindex = 0
        text = ""
        for tag in hashlist:
            text += "#" + tag + " "
            tag_el = {
                "tag": tag,
                "indices": [tindex, tindex+len(tag)]
            }
            #also counting # and space characters for indexing
            tindex += len(tag)+2
            tweet["entities"]["hashtag"].append(tag_el.copy())
        #some placeholder text in case the tweet has no text
        if len(text) == 0:
            text += "no_text"
        tweet["text"] = text

        tweetlist.append(tweet.copy())

    jsontweet = json.dumps(tweetlist)
    with open("out_twitgen.json", "w") as f:
        f.write(jsontweet)
        print("Output file is out_twitgen.json")

main()
