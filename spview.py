#!/usr/bin/python3
# Disclaimer: Python 3 used. Python 2 somehow refuses to install properly on my workstation

import datetime
import re
import requests


def get_episode_data(season, episode):
    """Returns dictionary with data for given episode or None when there is no such an episode"""
    req = requests.get(get_url_for_episode(season, episode))
    if req.status_code == 404:
        return None
    response = req.text
    # s/e
    ep = {'season': season, 'episode': episode}  # dictionary used instead of classes for simplicity only
    # title
    match = re.search("class=\"title\">([^<]+)", response)
    ep['title'] = match.group(1)
    # air date
    match = re.search("<span\s*class=\'air-date\'>([^<]+)", response)
    ep['aired'] = datetime.datetime.strptime(match.group(1), "%B %d, %Y")
    # wiki page
    match = re.search("href=\"([^<]+)\" title=\"Read wiki\"></a>", response)
    ep['wiki'] = match.group(1)
    # description
    match = re.search("</header>\s*<p class=\"\">([^<]+)</p>\s*</article>", response)
    ep['description'] = match.group(1)
    return ep


def get_url_for_episode(season, episode):
    """Creates URL for request. The URL parser at the server is quite straightforward - it reads only the first 6
    characters of the episode name which is simply s##e##"""
    return "http://southpark.cc.com/full-episodes/s{0:02d}e{1:02d}".format(season, episode)


def get_episodes(start=1, end=99):
    """Downloads data from given seasons"""
    eps = []
    season = start-1
    while season < end:
        season += 1
        ep = get_episode_data(season, 1)
        if not ep:  # no first episode ergo last season
            break
        eps.append([ep.copy()])
        curr_ep = 1
        while True:
            curr_ep += 1
            ep = get_episode_data(season, curr_ep)
            if not ep:
                break
            eps[-1].append(ep.copy())
    return eps


def fancy_episode(ep):
    if not ep:
        return "No such an episode: S{0:02d}E{1:02d}".format(ep['season'], ep['episode'])
    return '\n'.join(("South Park S{0:02d}E{1:02d}".format(ep['season'], ep['episode']),
                      "Title:".ljust(15) + ep['title'],
                      "First aired:".ljust(15) + ep['aired'].date().isoformat(),
                      "SP Wiki:".ljust(15) + ep['wiki'],
                      "Description:".ljust(15) + ep['description'],
                      "\n\n"))


def print_hello():
    return '\n'.join(("South Park episode lister",
                      "https://github.com/phreme/spview",
                      "Piotr 'phreme' Balbier, April 2015 OOP classes exercise\n\n"))

if __name__ == "__main__":
    with open("spout.txt", "w") as f:
        f.write(print_hello())
        eps = get_episodes()
        eps_flat = [x for season in eps for x in season]
        episode_count = len(eps_flat)
        season_count = len(eps)
        f.write("Received {0} episodes from {1} season(s)\n\n".format(episode_count, season_count))
        for ep in eps_flat:
            f.write(fancy_episode(ep))