import praw
from praw.models import MoreComments
import pandas as pd

# get data for each subreddit and store it in a csv

scraper = praw.Reddit(client_id="RpVq8mN7Alw8Lw", client_secret="4qHOHDX3Qs0iTxjrBOA_dr7JzteV1A", user_agent="CompLingScraper")

wsb_posts_scrape = []
wsb_raw = scraper.subreddit("wallstreetbets").top(limit=30)
for post in wsb_raw:
    post.comments.replace_more(0)
    for index, comment in enumerate(post.comments):
        print("wsb post %s comment %d" % (post.id, index))
        wsb_posts_scrape.append([post.id, post.subreddit, comment.body])
        if index == 30:
            break

wsb_posts = pd.DataFrame(wsb_posts_scrape, columns=["id", "subreddit", "body"])
wsb_posts.to_csv(r"wsb.csv")

ssb_posts_scrape = []
ssb_raw = scraper.subreddit("SatoshiStreetBets").top(limit=30)
for post in ssb_raw:
    post.comments.replace_more(0)
    for index, comment in enumerate(post.comments):
        print("ssb post %s comment %d" % (post.id, index))
        ssb_posts_scrape.append([post.id, post.subreddit, comment.body])
        if index == 30:
            break

ssb_posts = pd.DataFrame(ssb_posts_scrape, columns=["id", "subreddit", "body"])
ssb_posts.to_csv(r"ssb.csv")

crypto_posts_scrape = []
crypto_raw = scraper.subreddit("CryptoCurrency").top(limit=30)
for post in crypto_raw:
    post.comments.replace_more(0)
    for index, comment in enumerate(post.comments):
        print("crypto post %s comment %d" % (post.id, index))
        crypto_posts_scrape.append([post.id, post.subreddit, comment.body])
        if index == 30:
            break

crypto_posts = pd.DataFrame(crypto_posts_scrape, columns=["id", "subreddit", "body"])
crypto_posts.to_csv(r"crypto.csv")

stocks_posts_scrape = []
stocks_raw = scraper.subreddit("Stocks").top(limit=30)
for post in stocks_raw:
    post.comments.replace_more(0)
    for index, comment in enumerate(post.comments):
        print("stocks post %s comment %d" % (post.id, index))
        stocks_posts_scrape.append([post.id, post.subreddit, comment.body])
        if index == 30:
            break

stocks_posts = pd.DataFrame(stocks_posts_scrape, columns=["id", "subreddit", "body"])
stocks_posts.to_csv(r"stocks.csv")
