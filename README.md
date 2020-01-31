# twitterweatherbot
A bot for tweeting the weather. 
---
Copy twitter_api_example.json to twitter_api.json and then fill in your keys. Do the same with the weather_api_example.json file.

You will also have to copy sftp_example.json to sftp.json. Then put your SFTP info in the sft.json file.

All config files are in the .gitignore, in order to avoid accidentally publishing credentials.

---

I have it set up so that I run tweet.py on an Ubuntu VM on one of my hypervisors. I run take_photo.sh on a Raspberry Pi Zero W running Raspbian, and it has SSH enabled and SFTP too. A dependency for the shell script is libimage-exiftool-perl. It also must have an SSH server running so that the Ubuntu Server VM can log in and download the photo. 

The Raspberry Pi Zero W has a camera that takes pictures of the sky using raspistill. 

I guess you could technically try all of this on a single machine, but a Raspberry Pi Zero isn't very powerful, and I started this project as a VM on a hypervisor rather than something that has direct access to a camera. So the Zero W is mostly because it can use a camera. 

Before the addition of the Raspberry Pi Zero W and the take_photo.sh shell script, it would just tweet the weather text from the OpenWeatherMap current weather data API. But now it also takes a picture of the sky and tweets that too, albiet in a semi-convoluted way.

It also helps to create a static DHCP reservation for the SFTP server. 

Do not run the tweet.py script directly. Instead, put it in your crontab. 

Here are instructions for crontab: [Link](https://github.com/0x416c616e/twitterweatherbot/blob/master/crontab.md)

