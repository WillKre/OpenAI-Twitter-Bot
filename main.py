import tweepy
import json
import openai
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

def summariseTweet(tweet):
    """
    Summarises the parent tweet by using an instruction tuned large language model (LLM).

    Args:
        tweet (tweepy.Tweet): A Tweepy Tweet object representing the tweet to summarise.

    Returns:
        str: A summarised version of the tweet's text.
    """

    openai.api_key = credentials['open_ai']
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarise/Explain in a condensed way the following content in one or two short sentences with a total of no more than 200 characters:"},
            {"role": "user", "content": tweet.data.text}
        ]
    )
    summarised_tweet = completion.choices[0].message.content
    print(f"Summarised tweet is: {summarised_tweet}")
    return summarised_tweet

def respondToTweet(parent_tweet_id, summarised_tweet):
    """
    Creates a tweet in response to the parent.

    Args:
        parent_tweet_id: The id of the parent tweet.
        summarised_tweet: A summarised version of the tweet's text.
    """

    client = getTweepyClient()

    client.create_tweet(
        text=summarised_tweet,
        in_reply_to_tweet_id=parent_tweet_id
    )
    print(f"Successfully responded to tweet: {parent_tweet_id}")


def respondToTweets(tweets):
    """
    Fetches the "parent tweet" (either the tweet that is quoted or the tweet that is replied to), and replies with a summary.

    Args:
        tweets (tweepy.Response): A Tweepy response object containing the tweets to respond to.
    """

    client = getTweepyClient()

    if tweets.data is not None:
        for tweet in tweets.data:
            if hasattr(tweet, 'referenced_tweets') and tweet.referenced_tweets is not None:
                for ref_tweet in tweet.referenced_tweets:
                    parent_tweet = client.get_tweet(ref_tweet.id)
                    print(f"Parent tweet is: {parent_tweet.data.text}")
                    summarised_tweet = summariseTweet(parent_tweet)
                    respondToTweet(parent_tweet.data.id, summarised_tweet)
            else:
                print(f"Unable to retrieve parent tweet for tweet id: {tweet.data.id}")
    else:
        print("No tweets found!")


credentials = get_secrets_from_secrets_manager('summarise-gpt-prod')

tweets = getTweets();
respondToTweets(tweets);
