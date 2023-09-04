import json
import praw
import requests

credentials = 'client_secrets.json'
 
with open(credentials) as f:
    creds = json.load(f)


reddit = praw.Reddit(client_id=creds['client_id'],
                     client_secret=creds['client_secret'],
                     user_agent=creds['user_agent'],
                     redirect_uri=creds['redirect_uri'],
                     refresh_token=creds['refresh_token'])

subr = 'pythonsandlot' # Choose your subreddit
 
subreddit = reddit.subreddit(subr) # Initialize the subreddit to a variable
 
title = 'Just Made My first Post on Reddit Using Python.'

# TODO: Post images that are added to the base
selftext = '''
I am learning how to use the Reddit API with Python using the PRAW wrapper.
By following the tutorial on https://www.jcchouinard.com/post-on-reddit-api-with-python-praw/
This post was uploaded from my Python Script
'''

subreddit.submit(title,selftext=selftext)