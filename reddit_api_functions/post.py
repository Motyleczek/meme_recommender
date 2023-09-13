import json
import praw
import requests
import os

'''https://www.reddit.com/r/pythonsandlot/'''

def post(file, title):

    # credentials = r'client_secrets.json'
    
    # with open('meme_recommender\reddit_api_functions\client_secrets.json', 'r') as f:
    #     creds = json.load(f)

    # reddit = praw.Reddit(client_id=creds['client_id'],
    #                     client_secret=creds['client_secret'],
    #                     user_agent=creds['user_agent'],
    #                     redirect_uri=creds['redirect_uri'],
    #                     refresh_token=creds['refresh_token'])

    reddit = praw.Reddit(client_id="5TkuB1ByyLa_JeKw81qNxg",
                        client_secret="gxE-ssZaFp-SJ0_bGu0yD7P9QE5cxw",
                        user_agent="script by u/yourusername",
                        redirect_uri="http://localhost:8080",
                        refresh_token="1047299639039-mAHX37Xh98R1yrgG6C_IzGtyl8lu9w")
    
    subr = 'pythonsandlot' # Choose your subreddit
    
    subreddit = reddit.subreddit(subr) # Initialize the subreddit to a variable
    

    # TODO: Post images that are added to the base
    # selftext = '''
    # I am learning how to use the Reddit API with Python using the PRAW wrapper.
    # By following the tutorial on https://www.jcchouinard.com/post-on-reddit-api-with-python-praw/
    # This post was uploaded from my Python Script
    # '''
    submitted_post = subreddit.submit_image(title, image_path=file)

    return submitted_post.url

# if __name__ == "__main__":

    # post('titi', "title")