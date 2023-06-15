import tweepy
import json
import boto3
from botocore.exceptions import ClientError

# Get Secrets from AWS Secrets Manage
def get_secrets_from_secrets_manager(secret_name):
    secret_name = secret_name
    region_name = "eu-west-1"
    service_name = 'secretsmanager'

    session = boto3.session.Session()
    client = session.client(
        service_name=service_name,
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']

    return json.loads(secret)

def getTweepyClient():
    return tweepy.Client(
        bearer_token=credentials['bearer_token'],
        consumer_key=credentials['consumer_key'],
        consumer_secret=credentials['consumer_secret'],
        access_token=credentials['access_token'],
        access_token_secret=credentials['access_token_secret']
    )

# Get Recent Tweets via Tweepy
def getTweets():
    client = getTweepyClient()
    bot_name = 'SummariseGPT'
    query = f"@{bot_name}"
    max_results = 10

    # referenced_tweets is required to get the "parent" tweet content (either the tweet that got quoted, or replied to)
    return client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["referenced_tweets"])

def respondToTweets(tweets):
    client = getTweepyClient()

    if tweets.data is not None:
        for tweet in tweets.data:
            print(f"Tweet is: {tweet.text}")
            print(f"Keys are: {', '.join([attr for attr in dir(tweet) if not attr.startswith('_')])}")

            # Check if the tweet is a reply or a quote
            if hasattr(tweet, 'referenced_tweets') and tweet.referenced_tweets is not None:
                for ref_tweet in tweet.referenced_tweets:
                    # Fetch the parent tweet data
                    parent_tweet = client.get_tweet(ref_tweet.id)
                    print(f"Parent tweet is: {parent_tweet.data.text}")
            else:
                print(f"Unable to retrieve parent tweet for tweet id: {tweet.id}")

    else:
        print("No tweets found!")

credentials = get_secrets_from_secrets_manager('summarise-gpt-prod')

print(f"Credentials keys from get_secrets_from_secrets_manager: {list(credentials.keys())}")

tweets = getTweets();
    
print(f"Tweet from getTweets: {tweets}")

respondToTweets(tweets);
