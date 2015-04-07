#!/usr/bin/python3
# Disclaimer: Python 3 used. Python 2 somehow refuses to install properly on my workstation

import re
import requests


def get_episode_data(season, episode):
    """Returns dictionary with data for given episode or None when there is no such an episode"""
    req = requests.get(get_url_for_episode(season, episode))
    if req.status_code == 404:
        return None
    response = req.text
    # s/e
    ep = {'season': season, 'episode': episode}
    # title
    match = re.search("class=\"title\">([^<]+)", response)
    ep['title'] = match.group(1)
    # air date
    # match = re.search("class=\"air-date\">([^<]+)", response) # TODO: Still some problems
    # ep['aired'] = match.group(1)
    # description
    match = re.search("</header>\s*<p class=\"\">([^<]+)</p>\s*</article>", response)
    ep['description'] = match.group(1)
    return ep


def get_url_for_episode(season, episode):
    """Creates URL for request. The URL parser at the server is quite straightforward - it reads only the first 6
    characters of the episode name which is simply s##e##"""
    return "http://southpark.cc.com/full-episodes/s{0:02d}e{1:02d}".format(season, episode)


def list_episodes():
    pass


def print_hello():
    print("South Park episode lister")
    print("https://github.com/phreme/spview")
    print("Piotr 'phreme' Balbier, 2015 OOP classes exercise")

# if __name__ == "main":
print_hello()
print(get_episode_data(1, 3))