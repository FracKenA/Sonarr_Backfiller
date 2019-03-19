# Sonarr Backfiller
This script is intended to allow you to query your backlog of missing episodes without having to do them 10 at a time or all at once.

## Required to be installed
 - Python 2.7
 - requests module
 - json module
 - urlparse module 
 - PyYAML module
 
## Usage

 1. Download to desired location
 2. make executable 
  `# chmod a+x sonarr_backfiller.py`
 3. Put your Edit yaml file to suit your needs
 4. Execute Script
 
 You can create a cron task to execute this, however don't select too many at once. I will be adding additional checks and a check of the current queue status at a later date. 


Pull Requests are always welcome.
