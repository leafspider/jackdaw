import pytest, asyncio
from sparrow.toolkit.generate.tweet_generator import TweetGenerator
import json


@pytest.mark.asyncio
async def test_gen_text():

    topics = ["artificial intelligence"]

    gen = TweetGenerator()

    for topic in topics:
        tweet = gen.generate_text(topic)
        print("-" * 50)
        print(tweet)
        assert(len(tweet) > 0)
    
@pytest.mark.asyncio
async def test_gen_dataset():
    
    from os import getcwd, makedirs
    from os.path import exists

    base_path = getcwd() + '/data/tweets'
    if not exists(base_path):
        makedirs(base_path)

    topics = ["artificial intelligence", "space exploration", "climate change"]

    gen = TweetGenerator()

    for topic in topics:

        num_tweets = 1
        dataset = gen.generate_dataset(topic, num_tweets)
        
        # Save to file
        with open( base_path + "/" + topic + ".json", "w") as f:
            json.dump(dataset, f, indent=2)
            print(f"Generated {num_tweets} tweets and saved to {topic}'.json'")
        
        