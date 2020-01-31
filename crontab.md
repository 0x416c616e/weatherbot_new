# Instructions for scheduling the weather bot's tweets

## Background

This program used to use a loop and time.sleep() for doing task schedling. 

So it would run at 6am, then noon, then 6pm, and then repeat over and over again. The program would run, wait 6 hours, then run again, then wait 12 hours, and then loop. However, the problem with the sleep method of scheduling is that the script would take a few seconds to a minute to run, so every day, it would get farther and farther off schedule. So first it would be 6:00am, 12:00pm, and 6:00pm, and then 6:01am, 12:01pm, 6:02pm, then 6:02am, 12:03pm, 6:04pm, and so on. Eventually, it could be an hour off! That's not good.

## The new way of task scheduling for this project

There is a better way to schedule tasks in Linux: cron. Cron is a way to schedule tasks. The list of cron tasks is in a table, called the cron table, or crontab for short.

## Step 1

In order to edit the cron table, use the following command:

```
crontab -e
```

## Step 2

Now add this line in order to make the script run at 6am, 12pm, and 6pm:

```
0 6,12,18 * * * cd /home/alan/twitterweatherbot/ && /usr/bin/python3 /home/alan/twitterweatherbot/tweet.py
```

Replace "alan" with whatever your user account name is, and maybe change the path too, if you cloned the repo in a different directory aside from your home one.

Because tweet.py uses relative paths for some things, your crontab task needs to cd before running the program.
