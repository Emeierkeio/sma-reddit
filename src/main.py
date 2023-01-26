import os
import reddit
import pandas as pd
import logging
import sys

def run():
    # Configure reddit requests
    logging.info('Configuring reddit')
    requests = reddit.configure()

    thread = sys.argv[1]

    # Get the top 500 posts from the subreddit and return three lists
    logging.info('Getting the top 500 posts')
    subreddit = requests.subreddit(thread)
    top_subreddit = subreddit.top(limit=500)

    topics_dict = { "id":[], "title":[], "score":[], "url":[], "comms_num": [], "created": [], "body":[]}

    logging("Creating dataframe")
    i = 1
    for submission in top_subreddit:
        logging.info('Appending {} post'.format(i))
        topics_dict["title"].append(submission.title)
        topics_dict["score"].append(submission.score)
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["comms_num"].append(submission.num_comments)
        topics_dict["created"].append(submission.created)
        topics_dict["body"].append(utils.remove_commas(submission.selftext))
        i = i + 1

    # Take the url of each post and scrape the comments
    logging.info('Getting comments')
    comments = pd.DataFrame()
    for url in posts.url:
        try:
            logging.info(f'Getting comments from {url}')
            comments = pd.concat([comments, reddit.get_comments_df(url, requests.submission(url=url))])

        except Exception as e:
            logging.info(f'Error getting comments from {url}')
            logging.info(e)

    # Change the created_utc column to datetime
    comments['created_utc'] = pd.to_datetime(comments['created_utc'], unit='s')

    # Remove duplicates
    comments = comments.drop_duplicates()
    
    # Save the dataframes
    logging.info('Saving dataframes')
    posts.to_csv(os.path.join('../data/{}/posts.csv'.format(thread)), index=False)
    comments.to_csv(os.path.join('../data/{}/comments.csv'.format(thread)), index=False)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    run()