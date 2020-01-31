#!/usr/bin/python3
# Alan's Weather bot for Twitter
# You will need API keys for Twitter and OpenWeatherMap

# copy twitter_api_example.json to twitter_api.json
# and put your keys/tokens in there

# copy weather_api_example.json to weather_api.json
# and put your openweathermap api key there

# .gitignore will ignore the real config files with your keys
# don't put then on github!
# requires exiftool for shell script
# also requires pysftp from pip3


import sys
import os
import tweepy
import urllib.request
import json
import datetime
import time
import pysftp

# function for checking if a key is not properly loaded
# return true = key is good
# return false = key is bad
def check_loaded(key):
    return (not ((key == "NOTLOADED") or (key == "")))


def main():
    
    #get the credentials from the sftp.json file for the SFTP connection
    stfp_ip_address = "NOTLOADED"
    stfp_username = "NOTLOADED"
    sftp_password = "NOTLOADED"
    sftp_file = "sftp.json"
    if (os.path.exists(sftp_file)):
        #loading SFTP info from sftp.json config file
        print("SFTP file exists")
        try:
            with open(sftp_file, "r") as sftp_open:
                sftp_json = json.load(sftp_open)
                sftp_ip_address = sftp_json["ip_address"]
                sftp_username = sftp_json["username"]
                sftp_password = sftp_json["password"]
        except IOError:
            print("IOError with sftp.json")
            sys.exit()
        #finished loading SFTP JSON, now need to validate it
        print("Finished loading SFTP configs, now validating...")
        sftp_check_1 = check_loaded(sftp_ip_address)
        sftp_check_2 = check_loaded(sftp_username)
        sftp_check_3 = check_loaded(sftp_password)
        sftp_valid = sftp_check_1 and sftp_check_2 and sftp_check_3
        if (sftp_valid):
            print("SFTP settings are valid")
        else:
            print("Error with SFTP config validation, are they blank or default?")
            sys.exit()
    else:
        print("Error loading sftp credential file, did you copy sftp_example.json to sftp.json?")
        print("You also need to fill out the info in the sftp.json file")
        sys.exit()
    #opening the SFTP connection
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(sftp_ip_address, username=sftp_username, password=sftp_password, cnopts=cnopts) as sftp: 
        with sftp.cd('/home/pi'):
            sftp.get('sky.jpg')
            #download sky photo for weather

    #adding the timestamp and text to the sky.jpg image before posting int
    #if python3 means python3 on your computer, make python_ver = "python3"
    #but if python means python3 on your computer, make python_ver = "python"
    python_ver = "python3"
    command_string = python_ver + " image.py --filename=sky.jpg --size=64 --text=@ChiWeather"
    os.system(command_string)


    # variables for keys
    consumer_key = "NOTLOADED"
    consumer_secret = "NOTLOADED"
    access_token = "NOTLOADED"
    access_token_secret = "NOTLOADED"
    weather_api_key = "NOTLOADED"

    # variables for key file names
    # if you use encrypted storage, you might want to change these
    twitter_file = "twitter_api.json"
    weather_file = "weather_api.json"

    # check if required json files exist
    files_exist = (os.path.exists(weather_file) and os.path.exists(twitter_file))
    weather_api_json = ""
    twitter_api_json = ""
    if files_exist:
        print("Passed initial file checks")
        # loading weather api key from file
        try:
            with open(weather_file, "r") as fopen:
                weather_api_json = json.load(fopen)
                weather_api_key = weather_api_json["api_key"]
        except IOError:
            print(weather_file + " IOError")
            sys.exit()
        print("Finished loading Weather key")

        # loading twitter_api_keys from file
        try:
            with open(twitter_file, "r") as fopen:
                twitter_api_json = json.load(fopen)
                consumer_key = twitter_api_json["api_key"]
                consumer_secret = twitter_api_json["api_secret_key"]
                access_token = twitter_api_json["access_token"]
                access_token_secret = twitter_api_json["access_token_secret"]
        except IOError:
            print(twitter_file + " IOError")
            sys.exit()
        print("Finished loading Twitter keys")

        # checking stuff got loaded correctly
        check1 = check_loaded(consumer_key)
        check2 = check_loaded(consumer_secret)
        check3 = check_loaded(access_token)
        check4 = check_loaded(access_token_secret)
        check5 = check_loaded(weather_api_key)

        keys_valid = check1 and check2 and check3 and check4 and check5
        if keys_valid:
            print("Keys passed check")
            # Twitter API authentication using Tweepy
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            print("Successfully authenticated")
            # got some help from here: https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script

            # piecing together API request for weather data
            api_request_first_part = "https://api.openweathermap.org/data/2.5/weather?q="
            api_request_location = "Chicago"
            api_key_part = "&appid="
            api_request_units = "&units=imperial"

            # "weather" is the full API call
            weather = api_request_first_part + api_request_location + api_key_part + weather_api_key + api_request_units

            # downloading weather json data
            with urllib.request.urlopen(weather) as url:
                json_data = json.loads(url.read().decode())
                print("JSON data:")
                print(json_data)

            print("Finished downloading weather data")
            # getting data from the json
            # some of which is nested multiple times
            main_json = json_data["main"]
            temp = main_json["temp"]
            weather_json = json_data["weather"]
            temp_min = main_json["temp_min"]
            temp_max = main_json["temp_max"]
            humidity = main_json["humidity"]
            wind = json_data["wind"]
            wind_speed = wind["speed"]
            description_json = weather_json[0]
            description = description_json["description"]
            print("Building tweet string")

            now = datetime.datetime.now().strftime("%I:%M%p")

            # building the tweet text
            first_string = "As of " + now
            first_string += ", it is currently " + str(int(temp)) + " F in Chicago. High of "
            first_string += str(int(temp_max)) + " F and low of " + str(int(temp_min)) + " F. "
            first_string += str(int(humidity)) + "% humidity. "
            first_string += str(int(wind_speed)) + " mph wind. "
            second_string = "The weather is " + description + "."
            final_tweet = first_string + second_string

            # send the weather tweet
            api.update_with_media("sky.jpg",final_tweet) #send tweet
            current_time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
            print("Sent the following tweet at " + current_time + "")
            print("\"" + final_tweet + "\"")

        else:
            print("missing api key files")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nQuitting. Goodbye.")
        sys.exit()
