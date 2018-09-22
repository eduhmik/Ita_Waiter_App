import urllib
import json

TOKEN = "71c5fe0f100c1dac737085e6454b4ebc6c4da5aa"
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v4/shorten?access_token={}&longUrl={}"

class BitlyHelper:

    def shorten_url(self, longUrl):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN, longUrl)
            response = urllib.request.urlopen(url).read()
            jr = json.loads(response)
            return jr['data']['url']
        except Exception as e:
            print (e)