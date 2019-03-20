#!/usr/bin/env python2

# Written for python 2.7
# This script is used for triggering a search in Sonarr for a specific numner of episodes


# Stdlib
import urlparse
import logging
import datetime

# 3rf Party
import yaml
import requests


with open("sonarr_backfiller.yaml", "r") as settings_file:
    settings_import = yaml.safe_load(settings_file)

# TODO Add Error Checking
# TODO Add propper logging


def get_queue():
    api_endpoint = "/api/queue"
    uri_endpoint = urlparse.urljoin(settings_import["sonarr"]["address"], api_endpoint)
    headers = {
        'X-Api-Key': settings_import["sonarr"]["api_key"]
    }
    request_response = requests.get(uri_endpoint, headers=headers)

    logging.debug('request response url: %s', request_response.url)
    logging.debug('request response headers: %s', request_response.headers)
    logging.debug('request response encoding: %s', request_response.apparent_encoding)
    logging.debug('request response text: %s', request_response.text)
    logging.info('request response reason: %s', request_response.reason)
    logging.info('request response status code: %s', request_response.status_code)
    logging.info('request response time elapsed: %s', request_response.elapsed)

    json_response = request_response.json()
    download_queue = len(json_response)
    return download_queue


def get_wanted():
    episode_id_list = []
    api_endpoint = "/api/wanted/missing"
    uri_endpoint = urlparse.urljoin(settings_import["sonarr"]["address"], api_endpoint)
    headers = {
        'X-Api-Key': settings_import["sonarr"]["api_key"]
    }
    query = {"sortKey": "airDateUtc", "sortDir": settings_import["sonarr"]["sort_direction"],
             "pageSize": settings_import["sonarr"]["number_of_results"]}
    request_response = requests.get(uri_endpoint, params=query, headers=headers)

    logging.debug('request response url: %s', request_response.url)
    logging.debug('request response headers: %s', request_response.headers)
    logging.debug('request response encoding: %s', request_response.apparent_encoding)
    logging.debug('request response text: %s', request_response.text)
    logging.info('request response reason: %s', request_response.reason)
    logging.info('request response status code: %s', request_response.status_code)
    logging.info('request response time elapsed: %s', request_response.elapsed)

    json_response = request_response.json()
    for episode_id in json_response["records"]:
        episode_id_list.append(episode_id['id'])
    return episode_id_list


def queue_search(episode_list):
    api_endpoint = "/api/Command"
    uri_endpoint = urlparse.urljoin(settings_import["sonarr"]["address"], api_endpoint)
    headers = {
        'content-type': 'application/json',
        'X-Api-Key': settings_import["sonarr"]["api_key"]
    }
    payload = episode_list
    request_response = requests.post(uri_endpoint, headers=headers, json=payload)

    logging.debug('request submit uri %s', uri_endpoint)
    logging.debug('request submit headers %s', headers)
    logging.debug('request submit payload %s', payload)
    logging.debug('request response url: %s', request_response.url)
    logging.debug('request response headers: %s', request_response.headers)
    logging.debug('request response encoding: %s', request_response.apparent_encoding)
    logging.debug('request response text: %s', request_response.text)
    logging.debug('request response reason: %s', request_response.json)
    logging.info('request response reason: %s', request_response.reason)
    logging.info('request response status code: %s', request_response.status_code)
    logging.info('request response time elapsed: %s', request_response.elapsed)

    request_output = request_response.json()
    logging.info("Command ID = %s", request_output["id"])
    logging.info("Command State = %s", request_output["state"])


def main():

    log_entry_format = ':'.join(
        [
            '%(asctime)s',
            '%(levelname)s',
            '%(filename)s',
            '%(funcName)s',
            '%(lineno)s',
            '%(message)s',
        ]
    )

    logging.basicConfig(
        format=log_entry_format,
        level=logging.INFO,
        filename=".".join(
            [
                settings_import["logging_file_name"],
                datetime.datetime.now().strftime("%Y-%m-%d"),
                "log"
            ]
        )
    )

    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.INFO)
    requests_log.propagate = True

    queue_length = get_queue()
    if queue_length < settings_import["sonarr"]["queue_minimum"]:
        logging.info("Queue length is %s adding an additional %s items",
                     queue_length,
                     settings_import["sonarr"]["number_of_results"]
                     )
        episode_list = {"name": "EpisodeSearch"}
        episode_list.update({"EpisodeIds": get_wanted()})
        queue_search(episode_list)
    else:
        logging.info("Queue length is %s which exceeds limit os %s to add additional items",
                     queue_length,
                     settings_import["sonarr"]["number_of_results"]
                     )


if __name__ == '__main__':
    main()
