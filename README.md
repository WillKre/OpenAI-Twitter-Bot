# OpenAI Twitter Bot

This Twitter bot utilizes the Tweepy API, OpenAI and AWS (Secrets Manager & DynamoDB) to interact with tweets when tagged. This bot is configurable and can perform various tasks based on the prompt provided.

*Note: This bot uses Tweepy's `search_recent_tweets()` function in a polling manner to periodically check for tags and respond. The reason for this is that the Stream API, which provides real-time tweet updates comes with a substantial cost ($5000/month).*

## Demo

![demo](https://github.com/WillKre/OpenAI-Twitter-Bot/assets/7396157/88132454-3572-4868-bd22-4b31d9411e3f)

## Prerequisites

1. AWS Account with access to AWS Secrets Manager and DynamoDB.
2. OpenAI account with access to the API.
3. Twitter Developer Account (Basic) to access the Twitter API via Tweepy.

## Setup 

### AWS Secrets Manager

Store your OpenAI key, Twitter Bearer token, and Tweepy API keys in AWS Secrets Manager in the following format:

```json
{
    "bearer_token": "<your-twitter-bearer-token>",
    "consumer_key": "<your-twitter-consumer-key>",
    "consumer_secret": "<your-twitter-consumer-secret>",
    "access_token": "<your-twitter-access-token>",
    "access_token_secret": "<your-twitter-access-token-secret>",
    "open_ai": "<your-openai-key>"
}
```

### DynamoDB

Create a DynamoDB table where the primary key is `tweet_id` (String).

### Install Dependencies 

Install the necessary libraries:

```bash
pip3 install tweepy boto3 openai
```

### Running the Bot 

Modify the `main.py` file to configure the bot according to your needs. Change the `bot_name`, `chat_gpt_model`, `prompt_prefix`, AWS resource names, and AWS region according to your setup.

Run the bot:

```bash
python3 main.py
```

## Code Overview

The code consists of two Python scripts:

1. `main.py`: This is the main script to run the bot. It configures the bot and polls for tweets and responds to them.

2. `tweet_bot.py`: This script contains the `OpenAIBot` class which encapsulates all the bot functionality.

### How does the bot work?

1. The bot fetches the credentials from AWS Secrets Manager and sets up the Tweepy client and the DynamoDB client.
2. The bot periodically fetches recent tweets mentioning the bot's name.
3. For each tweet, it checks if the bot has already responded to the tweet by querying the DynamoDB database. If it has not responded, it fetches the parent tweet (the tweet that is either quoted or replied to).
4. It processes the parent tweet using the OpenAI model based on the prompt defined in the `main.py`.
5. It then replies to the original tweet (which mentioned the bot) with the processed text.
6. The tweet id is then added to the DynamoDB database to ensure the bot does not respond to the same tweet again.
