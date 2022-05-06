from geopy.geocoders import Nominatim
from textblob import TextBlob
import json
from elasticsearch import Elasticsearch

# instantiate a new Nominatim client
app = Nominatim(user_agent="tutorial")

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
        print(field)
        tmp = field.split(":") 
        key = tmp[0]
        value = ":".join(tmp[1:])
        res[key] = value
        
    json_res = json.dumps(res, indent=3)
    
    es = Elasticsearch("http://host.docker.internal:9200") # Same port when running elasticsearch with docker
    es.index(index="test",
             id=1, 
             document=json_res)
    return json_res