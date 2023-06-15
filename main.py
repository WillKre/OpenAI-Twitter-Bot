import tweepy
import json
import boto3
from botocore.exceptions import ClientError

def get_secrets_from_secrets_manager(secret_name):
    """
    Retrieves secrets from AWS Secrets Manager.

    Args:
        secret_name (str): The name of the secret to retrieve.

    Returns:
        dict: The secrets as a dictionary.

    Raises:
        ClientError: If the secrets could not be retrieved.
    """

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

    return json.loads(get_secret_value_response['SecretString'])


def getTweepyClient():
    """
    Constructs and returns a Tweepy client configured with the provided credentials.

    Returns:
        tweepy.Client: A Tweepy client.
    """

    return tweepy.Client(
        bearer_token=credentials['bearer_token'],
        consumer_key=credentials['consumer_key'],
        consumer_secret=credentials['consumer_secret'],
        access_token=credentials['access_token'],
        access_token_secret=credentials['access_token_secret']
    )


def getTweets():
    """
    Searches and returns recent tweets mentioning the bot.

    Returns:
        tweepy.Response: A Tweepy response object containing the found tweets.
    """

    client = getTweepyClient()
    bot_name = 'SummariseGPT'
    query = f"@{bot_name}"
    max_results = 10

    return client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["referenced_tweets"])


def respondToTweets(tweets):
    """
    Prints the content of the provided tweets and any associated parent tweets.

    Args:
        tweets (tweepy.Response): A Tweepy response object containing the tweets to respond to.
    """

    client = getTweepyClient()

    if tweets.data is not None:
        for tweet in tweets.data:
            print(f"Tweet is: {tweet.text}")

            # If the tweet references other tweets, retrieve and print their content as well
            if hasattr(tweet, 'referenced_tweets') and tweet.referenced_tweets is not None:
                for ref_tweet in tweet.referenced_tweets:
                    parent_tweet = client.get_tweet(ref_tweet.id)
                    print(f"Parent tweet is: {parent_tweet.data.text}")
            else:
                print(f"Unable to retrieve parent tweet for tweet id: {tweet.id}")
    else:
        print("No tweets found!")


credentials = get_secrets_from_secrets_manager('summarise-gpt-prod')

tweets = getTweets();
respondToTweets(tweets);
