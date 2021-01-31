import requests
import json
import utils
import sys
from logging import *

"""
This script to get Artist average Number of words in every song . 
"""

def getArtistmib(artistname):
    try:
        headers = {'Accept': 'application/json'}
        info("setting json info for header")
        params = 'query=%s&limit1&method=direct' % artistname
        result = requests.get('http://musicbrainz.org/ws/2/artist/', params=params, headers=headers)
        result = result.json()
        artistmib = result["artists"][0]['id']
        return artistmib
    except Exception as ex:
        print("Something went wrong , or Artist doesnot exists")
        error(ex)
        sys.exit(1)

def getsongDetails(atristmib):
    try:
        headers = {'Accept': 'application/json'}
        songparam = 'query=arid:%s' % artistmib
        info("Generating Song information for Artist" + artistname)
        songs = requests.get("http://musicbrainz.org/ws/2/recording/", params=songparam,headers=headers)
        #print(songs.url)
        songs = songs.json()
        songwordlist = []

        titles = set(utils.extract_values(songs["recordings"],"title"))
        info("Generating songs word count for artist" + artistname)
        for x in set(titles):
            x = str(x)
            wordcountjson = requests.get('https://api.lyrics.ovh/v1/%s/%s' % (artistname,x))
            if wordcountjson.status_code == 200:
                words = wordcountjson.json()
                if len(words["lyrics"]) != 0:
                    songwordlist = songwordlist + (words["lyrics"]).split()
                else:
                    titles.remove(x)
            else:
                pass
        return (len(songwordlist)/len(titles))
    except Exception as ex:
        print(ex)
        error(ex)
        sys.exit(1)


if __name__ == "__main__":
        basicConfig(filename='musicbenz.log', level=DEBUG)
        print("Input artist name")
        artistname = input()
        info("Getting information for " + artistname)
        artistmib = getArtistmib(artistname)
        print ("Number of average words per songs %s" % getsongDetails(artistmib))
        info("Number of average words per songs %s" % getsongDetails(artistmib))

