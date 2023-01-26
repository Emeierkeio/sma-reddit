import praw
import os
import pandas as pd
from praw.models import MoreComments
import logging
import secret


def configure():
    '''
    Configure the reddit requests

    params:
        None

    returns:
        reddit: Praw reddit object
    '''
    reddit = praw.Reddit(
        client_id=secret.CLIENT_ID,
        client_secret=secret.CLIENT_SECRET,
        user_agent="linux:com.example.myredditapp:v0.0.1 (by /u/USERNAME)",
        username=secret.USERNAME,
        password=secret.PASSWORD,
    )
    return reddit


def get_posts(reddit: praw.reddit.Reddit, subreddit: str) -> dict:
    '''
    Get the newest and hottest posts from the subreddit and return three lists
    
    params:
        reddit: Praw reddit object
        subreddit: Subreddit to scrape
        
    returns:
        hot_posts: List of hot posts
        new_posts: List of new posts
    '''
    logging.info(f'Getting posts from {subreddit}')
    logging.info('Hot posts')
    hot_posts = reddit.subreddit(subreddit).hot(limit=100)
    logging.info('New posts')
    new_posts = reddit.subreddit(subreddit).new(limit=100)

    # Create a list of dict with all the information
    logging.info('Changing submission to dict')

    return hot_posts, new_posts

def get_posts_df(hot_posts: praw.models.listing.generator.ListingGenerator, new_posts: praw.models.listing.generator.ListingGenerator) -> pd.DataFrame:
    '''
    Create a dataframe that contains the most important information from the posts from the lists
    
    params:
        hot_posts: Dict of hot posts
        new_posts: Dict of new posts
    
    returns:
        posts: Dataframe with the most important information from the posts
    '''
    
    logging.info('Creating post dataframe')

    # Create a pd dataframe with the most important information: title, selftext, author, upvote_ratio, ups, downs, score, num_comments, created_utc, url
    posts = pd.DataFrame(columns=['id', 'title', 'selftext', 'author', 'upvote_ratio', 'ups', 'downs', 'score', 'num_comments', 'created_utc', 'url'])

    for post in hot_posts:
        post.selftext = remove_commas(str(post.selftext))
        post.title = remove_commas(str(post.title))
        post.author = remove_commas(str(post.author))
        posts = pd.concat([posts, pd.DataFrame([[post.id, post.title, post.selftext, post.author, post.upvote_ratio, post.ups, post.downs, post.score, post.num_comments, post.created_utc, post.url]], columns=['id', 'title', 'selftext', 'author', 'upvote_ratio', 'ups', 'downs', 'score', 'num_comments', 'created_utc', 'url'])])  


    for post in new_posts:
        post.selftext = remove_commas(str(post.selftext))
        post.title = remove_commas(str(post.title))
        post.author = remove_commas(str(post.author))
        posts = pd.concat([posts, pd.DataFrame([[post.id, post.title, post.selftext, post.author, post.upvote_ratio, post.ups, post.downs, post.score, post.num_comments, post.created_utc, post.url]], columns=['id', 'title', 'selftext', 'author', 'upvote_ratio', 'ups', 'downs', 'score', 'num_comments', 'created_utc', 'url'])])  


    # Remove duplicates
    logging.info('Removing duplicates')
    posts = posts.drop_duplicates()

    return posts

def get_comments_df(url: str, submission: praw.models.reddit.submission.Submission) -> pd.DataFrame:
    '''
    Get the comments from the url return a dataframe with the comments.
    
    params:
        url: Url of the post from where to scrape the comments
        submission: Praw submission object
        
    returns:
        comments: Dataframe with all the comments of all posts
    '''

    df = pd.DataFrame(columns=['id', 'author', 'body', 'score', 'created_utc', 'parent_id', 'subreddit', 'subreddit_id', 'ups', 'downs', 'total_awards_received'])

    count = 1
    for comment in submission.comments[:300]:
        logging.info(f'Getting comment {count}')
        if isinstance(comment, MoreComments):
            continue
        comment.body = remove_commas(str(comment.body))
        comment.author = remove_commas(str(comment.author))
        df = pd.concat([df, pd.DataFrame([[comment.id, comment.author, comment.body, comment.score, comment.created_utc, comment.parent_id, comment.subreddit, comment.subreddit_id, comment.ups, comment.downs, comment.total_awards_received]], columns=['id', 'author', 'body', 'score', 'created_utc', 'parent_id', 'subreddit', 'subreddit_id', 'ups', 'downs', 'total_awards_received'])])  
        count += 1

    # Add a column with the post url
    df['post_url'] = url

    df.index = df['id']
    return df