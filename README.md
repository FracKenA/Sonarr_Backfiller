# Sonarr Backfiller
This script is intended to allow you to query your backlog of missing episodes without having to do them 10 at a time or all at once.

## Required to be installed
 - Python 2.7
 
Standard Library 
 - requests module
 - json module
 - urlparse module
 - datetime module
 
3rd Part Libraries Required 
 - PyYAML module
 - requests module
 
## Usage

Linux Directions (I am not providing directions for installing the 3rd party libraries)
```
# cd /opt # change this to your desired location 
# git clone https://github.com/FracKenA/Sonarr_Backfiller.git
# cp ./Sonarr_backfiller/sonarr_backfiller.yaml.sample ./Sonarr_Backfiller/sonarr_backfiller.yaml
```

Edit the yaml file replacing the api_key and address fields. You can also change the queue and active count before adding.
```
logging_level: "DEBUG"
logging_file_name: "sonarr_backfiller"
sonarr:
  sort_direction: "desc"
  number_of_results: 30
  api_key: "SONARR_API_KEY"
  address: "http://sonarr_address:port" 
  queue_minimum: 50
```



 1. Download to desired location
 2. make executable 
  `# chmod a+x sonarr_backfiller.py`
 3. Edit yaml file to match your Sonarr server
 4. Execute Script
 
 You can create a cron task to execute this, however don't select too many at once. I will be adding additional checks and a check of the current queue status at a later date. 


Pull Requests are always welcome.
