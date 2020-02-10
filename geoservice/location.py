import urllib
import requests


def get_coordinates(address):

    address_parsed = urllib.parse.quote(address)
    print("address_parsed")
    print(address_parsed)
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    querystring = {"address": address,
                   "key": "AIzaSyC4Gol1U3BbHLkWzeJb5kbggvFAPVKZRAA"}
    headers = {
        'User-Agent': "PostmanRuntime/7.20.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "maps.googleapis.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.get(url, headers=headers, params=querystring)
    try:
        geo_location = response.json()['results'][0]['geometry']['location']
    except:
        geo_location = {'lat': '4.624335', 'lng': '-74.063644'}

    return geo_location



