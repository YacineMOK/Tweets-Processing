from geopy.geocoders import Nominatim
from textblob import TextBlob
import json
from elasticsearch import Elasticsearch

# instantiate a new Nominatim client
app = Nominatim(user_agent="YacineLilia")

# Database - Link & create the 
es = Elasticsearch("http://host.docker.internal:9200") # Same port when running elasticsearch with docker

# If this is the first time  you run this code, the index may not exist, we have to create it
if ("filtered_tweets" not in es.indices.get_alias("*").keys()) :
    es.indices.create(index='filtered_tweets')

def get_location_by_address(address):
    """This function returns a location as raw from an address
    will repeat until success"""
    try:
        return app.geocode(address).raw['lat'], app.geocode(address).raw['lon']
    except:
        return None
    
    
# We create a function that analysis text with textblob
def sentiment(text):
    """ Function that returns -1 if a tweet is more likely negative (polarity<0)
                               0 if it's neutral  (polarity==0)
                               1 if it's positive (polarity>0)
    """
    polarity = TextBlob(text).polarity
    return 1 if polarity > 0 else -1 if polarity < 0 else 0


def tweetToJSON(tweeple):
    """
    TweePle (Tweet in the Tuple format)
    """
    res = {}
    for field in tweeple:
        tmp = field.split(":") 
        key = tmp[0] # Before the first :
        value = ":".join(tmp[1:]) # Join the remaining cells with ":"
        res[key] = value
        
    # Dump the dict
    json_res = json.dumps(res, indent=3)
    
    # Add this tweet to elasticsearch
    es.index(index="filtered_tweets",
             id=res["id"],
             document=json_res)
    
    return json_res