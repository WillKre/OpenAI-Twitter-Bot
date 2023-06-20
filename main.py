import time
from tweet_bot import OpenAIBot

if __name__ == "__main__":
    # Configure Bot
    bot_name = '' # Your Twitter bot name here
    chat_gpt_model = 'gpt-3.5-turbo'
    prompt_prefix = "You must summarise/explain in a condensed way the following content in one or two short sentences with a total of no more than 200 characters:"

    # Specify AWS resource names
    aws_region_name=''
    aws_secret_name=''
    aws_dynamodb_table_name=''
    
    # Instantiate Bot
    bot = OpenAIBot(bot_name, chat_gpt_model, prompt_prefix, aws_region_name, aws_secret_name, aws_dynamodb_table_name)

    while True:
        # Use Bot
        tweets = bot.get_tweets()
        bot.respond_to_tweets(tweets)
        time.sleep(30) # Update polling time here according to your API limit