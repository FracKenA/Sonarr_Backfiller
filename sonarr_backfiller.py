#!/usr/bin/env python2

import json
import urlparse
import yaml
import requests


with open("sonarr_backfiller.yaml", "r") as settings_file:
    sonarr_settings = yaml.safe_load(settings_file)


def get_wanted():
    episode_id_list = []
    sonarr_api_endpoint = "/api/wanted/missing"
    sonarr_uri_endpoint = urlparse.urljoin(sonarr_settings["sonarr_address"], sonarr_api_endpoint)
    sonarr_query = {"apikey": sonarr_settings["api_key"], "sortKey": "airDateUtc", "sortDir": sonarr_settings["sort_direction"], "pageSize": sonarr_settings["number_of_results"]}
    json_response = requests.get(sonarr_uri_endpoint, params=sonarr_query).json()
    for episode_id in json_response["records"]:
        episode_id_list.append(episode_id['id'])
    return episode_id_list


def queue_search(episode_list):
    sonarr_api_endpoint = "/api/Command"
    sonarr_uri_endpoint = urlparse.urljoin(sonarr_settings["sonarr_address"], sonarr_api_endpoint)
    sonarr_query = {"apikey": sonarr_settings["api_key"]}
    sonarr_headers = {'content-type': 'application/json'}
    sonarr_payload = episode_list
    json_response = requests.post(sonarr_uri_endpoint, params=sonarr_query, headers=sonarr_headers, json=sonarr_payload)
    request_output = json.loads(json_response.text)
    # TODO Add Error Checking
    print "Command ID = " + str(request_output["id"])
    print "Command State = " + request_output["state"]


def main():
    episode_list = {"name": "EpisodeSearch"}
    episode_list.update({"EpisodeIds": get_wanted()})
    queue_search(episode_list)
    # TODO Add API Call to check Queue Status and refresh as needed


if __name__ == '__main__':
    main()
