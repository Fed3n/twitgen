import json
import datetime
import time
import copy
import random
from shapely.geometry import Polygon, Point

##SETTINGS##This stuff should be in a config file but i can't be bothered rn
N_TWEETS = 100
N_USERS = 60
#CHANCE OF TWEETS WITH COMPLETE GEO (be careful geo can be very slow to process especially with large bounding boxes)
GEO_CHANCE = 0.4
#JSON FILE OF TWITTER'S 'PLACE' ARRAY [from where a random location will be equally chosen]
LOCATIONS_FILE = "citta_italia.json"
#ONE OR MORE HASHTAG PER TWEET [number is chance of each]
HASHTAGS = [["covid",0.3],["lockdown",0.2],["vaccino",0.1],["zona rossa",0.2]]
TIME_RANGE = ["2020-10-01", "2020-12-31"]
#ONE OR MORE DIRECT IMAGE URL PER TWEET [number is chance of each]
IMAGES = [["https://i.imgur.com/7tVYAeF.png",0.3],["https://i.imgur.com/4M8Tos4.png",0.2]]
#LIST OF USERNAME STRINGS, CAN BE ALSO EMPTY OR WITH LESS NAMES THAN USERS
NAMES = ["Mario", "Luigi"]
###########

#CONSTS
TWID_BASE = 1000000000000000000
TWID_MAX = 1999999999999999999
UID_BASE = 100000000
UID_MAX = 999999999
IMGID_BASE = 1000000000000000000
IMGID_MAX = 1999999999999999999
 


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

#given n and a list names of names, generates a list of users
def generate_users(n,names):
    users = []
    for i in range(n):
        #yes we could get two identical ids, no not changing it atm
        uid = UID_BASE + random.random() * (UID_MAX - UID_BASE)
        #if there are no more names available they are in the user+uid format
        if len(names) > 0:
            name = names.pop()
        else:
            name = f"user{int(uid)}"
        user = {
            "id": uid,
            "id_str": f"{int(uid)}",
            "name": name,
            "screen_name": name 
        }
        users.append(user) 
    return users

def get_random_date(daterange):
    start = time.mktime(time.strptime(daterange[0], "%Y-%m-%d"))
    end = time.mktime(time.strptime(daterange[1], "%Y-%m-%d"))
    rngtime = start + (random.random()*(end-start))
    return time.strftime("%a %b %d %H:%M:%S %z %Y", time.localtime(rngtime))
    

def parse_json():
    with open(LOCATIONS_FILE) as f:
        data = f.read()
        parsed = json.loads(data)
        return parsed

#https://stackoverflow.com/questions/55392019/get-random-points-within-polygon-corners
#given a twitter bounding box and n, generates n random points inside the boundaries 
#(slow algorithm, generates a viable point and checks if it's inside the boundaries)
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
    places = parse_json()
    users = generate_users(N_USERS,NAMES)
    for i in range(N_TWEETS):
        #progress countup :')))) you are gonna need it for sanity
        print(f"{i+1} tweets generated", end=("\n" if (i+1)>=N_TWEETS else "\r"))

        tweet = copy.deepcopy(TWEET)

        twid = TWID_BASE + random.random() * (TWID_MAX - TWID_BASE)
        tweet["id"] = twid
        tweet["id_str"] = f"{int(twid)}"

        tweet["created_at"] = get_random_date(TIME_RANGE)

        #there could be more tweets from same user
        tweet["user"] = random.choice(users)
        
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

        imglist = []
        for url in IMAGES:
            if random.random() <= url[1]:
                imglist.append(url[0])
        
        #tweet text and appending entities
        #every entity in a tweet has indices which identify at what point of the text it occurs
        tindex = 0
        text = ""
        for tag in hashlist:
            tag_el = {
                "tag": tag,
                "indices": [tindex, tindex+len(tag)]
            }
            text += "#" + tag + " "
            #also counting # and space characters for indexing
            tindex += len(tag)+2
            tweet["entities"]["hashtag"].append(tag_el.copy())
        
        if len(imglist) > 0:
            tweet["entities"]["media"] = []  
        for imgurl in imglist:
            imgid = IMGID_BASE + random.random() * (IMGID_MAX - IMGID_BASE)
            tweet["entities"]["media"].append({
                "id": imgid,
                "id_str": f"{int(imgid)}",
                #these two are the same rn sorry
                "media_url": imgurl,
                "media_url_https": imgurl,
                "indices": [tindex, tindex+len(tag)],
                "type": "photo"
                #no sizes as of yet
            })
            text += imgurl + " "
            #counting space
            tindex += len(imgurl)+1

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
