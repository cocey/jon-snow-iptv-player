import json
import os.path
import re

from pyxtream import XTream, Episode, Serie, Channel
from collections import Counter


class Stream:
    status = False
    isLoaded = False
    def login(self, server_name, username, password, url):
        self.serverName = server_name
        self.username = username
        self.password = password
        self.url = url
        self.xt = XTream(self.serverName, self.username, self.password, self.url)
        # self.load()
        self.status = self.xt.auth_data != {}
        return self.status

    def load(self):
        self.refresh()
        # if(os.path.exists('data.json')):
        #     with open('data.json', 'r') as file:
        #         self.data = json.load(file)
        # else:
        #     self.refresh()


    def save(self):
        with open('data.json', 'w') as file:
            json.dump(self.data, file)


    def refresh(self):
        if self.xt.auth_data != {}:
            self.xt.load_iptv()
            self.setData()
            self.save()
            self.isLoaded = True
        else:
            print("Could not connect")

    def setData(self):

        self.data = {
            "channels": [],
            "movies": [],
            "series": [],
        }
        self.series = {}

        for item in self.xt.channels:
            item: Channel = item
            self.data["channels"].append({"name": item.name, "url": item.url, "id": item.id, "type": "channel", "export":item.export_json()})

        for item in self.xt.movies:
            item: Channel = item
            self.data["movies"].append({"name": item.name, "url": item.url, "id":item.id, "type": "movie", "export":item.export_json()})

        for item in self.xt.series:
            item: Serie = item
            self.data["series"].append({"name": item.name, "url": item.url, "id":item.series_id, "type": "serie", "export":item.export_json()})
            if not item.series_id in self.series:
                self.series[item.series_id] = item


    def getData(self):
        return self.data

    def getChannels(self):
        return self.data["channels"]

    def getMovies(self):
        return self.data["movies"]

    def getSeries(self):
        return self.data["series"]

    def searchText(self, text):
        text = text.lower()

        result = {
            "channels": [],
            "movies": [],
            "series": []
        }

        for item in self.data["series"]:
            if text in item["name"].lower():
                result["series"].append(item)
        for item in self.data["movies"]:
            if text in item["name"].lower():
                result["movies"].append(item)
        for item in self.data["channels"]:
            if text in item["name"].lower():
                result["channels"].append(item)

        return result


    def search(self, text):

        result_ = self.searchText(text)
        result = {}
        for x in result_:
            if len(result_[x])>0:
                result[x] = result_[x]

        return result

    def getSerie(self, id):
        item: Serie = self.series[id]
        self.xt.get_series_info_by_id(item)
        result = {}
        i = 1
        for seasonKey in item.seasons:

            season = item.seasons[seasonKey]

            if not seasonKey in result:
                result[seasonKey] = []

            for episodeKey in season.episodes:
                episode: Episode = season.episodes[episodeKey]
                seasonNumber = self.getSeasonByName(episode.name)

                if not seasonNumber == i:
                    continue
                else:
                    result[seasonKey].append({"name": episode.name, "url": episode.url, "id":episode.id, "type":"episode"})
            i+=1

        return result

    def getVideo(self, id):
        id = int(id)
        print("get_download_progress", self.xt.get_download_progress(id))
        print("download_video", self.xt.download_video(id))

    def getSeasonByName(self, name):
        x = re.findall("S([0-9]+)E([0-9]+)", name)
        return int(x[0][0])


    def dump(self):
        for s in self.xt.series:
            print(s.name, s.url)