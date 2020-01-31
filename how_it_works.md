# How the weather bot works

## Architecture

The Raspberry Pi takes a photo from the attached camera using the take_photo.sh shell script. The Raspberry Pi is acting as an SFTP server.

There is an ESXi hypervisor with an Ubuntu Server VM on it. There are credential files on it that contain login info and configurations for the SFTP server, weather API, and Twitter API. They are in .gitignore so they can't be uploaded to GitHub. The Ubuntu VM uses crontab to schedule running tweet.py 3 times a day. tweet.py uses the SFTP credential file (sftp.json) to log into the Raspberry Pi SFTP server to download the photo taken by the camera. Then tweet.py uses image.py to put text on top of the image. It then queries the weather API, which returns JSON data about the weather, and then tweet.py parses the JSON and builds the tweet string. tweet.py authenticates with the Twitter API using Tweepy, and then creates a tweet containing the edited image and the text about the weather. Then the tweet it sent.
