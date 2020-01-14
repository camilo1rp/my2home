import urllib
import requests


def get_coordinates(address):
    address_parsed = urllib.parse.quote(address)
    print(address_parsed)
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    querystring = {"address": address_parsed, "key": "AIzaSyC4Gol1U3BbHLkWzeJb5kbggvFAPVKZRAA"}
    response = requests.request("GET", url, params=querystring)
    print(response.json()['results'][0]['geometry']['location'])
    return response.json()['results'][0]['geometry']['location']
