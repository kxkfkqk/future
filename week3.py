import urllib.request as req
import json

url="https://padax.github.io/taipei-day-trip-resources/taipei-attractions.json?fbclid=IwAR1er6RmImIlBl_H1XYQ7yI_ni2w-ppnw1iMs6ABq0ZFasJZ9toSwn7pFBg"
with req.urlopen(url) as response:
    data=json.load(response)
data=data["result"]["results"]
with open ("data.txt", mode="w", encoding="utf-8") as file:
    for name in data:
        img=name["file"]
        if "http" in img[1:]:
            goodimg="h"+img[1:][:img[1:].index("http")]
        else:
            goodimg=img
        totaldata=name["stitle"]+","+name["longitude"]+","+name["latitude"]+","+goodimg+"\n"
        file.write(totaldata)