import requests
import json
import string

def twitterSearch(search_term):
  encode_token = "Bearer" + " " + "AAAAAAAAAAAAAAAAAAAAAHRrzwAAAAAApZrEnfRevbxhGUyXLGtB0RD9lL8%3D9XABLtLey03WDb5F6bYYugN3t0SQeFIXau6aFSFUUeb4S3i30I"

  headers = {
    'Authorization': encode_token
  }

  search_term = search_term.replace(" ", "%20")

  search_url = "https://api.twitter.com/1.1/search/tweets.json?q=" + search_term + "&result_type=popular&count=10&lang=en&include_entities=false"

  r = requests.get(search_url, headers = headers)

  twitter_response = r.json()

  tweets = []
  counter = 1;

  for tweet in twitter_response['statuses']:
    tweet_id = str(tweet['id'])
    screen_name = str(tweet['user']['screen_name'])
    tweet_url = "https://twitter.com/" + screen_name + "/status/" + tweet_id
    tweets.append((tweet_url, counter))
    counter += 1

  return tweets
  
	
def visionCall(img_str):
    payload = {
            "requests": [
              {
                  "features": [
                  {
                    "type": "LOGO_DETECTION"
                  }, 
                  {
                    "type": "WEB_DETECTION"
                  }, 
                ],
                "image": {
                  "content": img_str
                }
              }
            ]
          };
          
    r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=AIzaSyBqg46sA99Iy8Nr2cs2FRTbIIKyrQzBEJY", data=json.dumps(payload))

    logo_info = r.json()

    if logo_info['responses'][0]['logoAnnotations'][0]['description']:
      result = logo_info['responses'][0]['logoAnnotations'][0]['description']
      if twitterSearch(result):
        return result
      
    if logo_info['responses'][0]['webDetection']['webEntities']:
      for entities in logo_info['responses'][0]['webDetection']['webEntities']:
        result = entities['description']
        if twitterSearch(result):
          return result

    return "No results for image. Try another image"




