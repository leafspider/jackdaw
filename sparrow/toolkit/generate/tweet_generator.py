from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

import random
# import json
from faker import Faker

class TweetGenerator:

    def __init__(s):

        # Initialize the model
        s.llm = OllamaLLM(model="llama3.1")  # any local model
        
        # Initialize for generating fake data
        s.fake = Faker()

        # Create a prompt template for generating tweets
        s.prompt = PromptTemplate(
            input_variables=["topic"],
            template="Generate a tweet about {topic} containing 280 characters or less."
        )

        # Create a chain
        s.chain = s.prompt | s.llm

    # Generate text
    def generate_text(s, topic):
        return s.clean(s.chain.invoke(topic))
    
    def clean(s, txt):
        return txt[1:len(txt)-1]
    
    # Generate a tweet
    def generate_json(s, topic):
        tweet = {
            "user": {
                "id": s.fake.random_number(digits=10),
                "name": s.fake.name(),
                "screen_name": s.fake.user_name(),
                "location": s.fake.city(),
                "followers_count": random.randint(0, 1000000),
                "friends_count": random.randint(0, 10000),
            },
            "id": s.fake.random_number(digits=19),
            "created_at": s.fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
            # "text": s.fake.text(max_nb_chars=280),
            "text": s.generate_text(topic),
            "retweet_count": random.randint(0, 10000),
            "favorite_count": random.randint(0, 20000),
            "lang": random.choice(["en", "es", "fr", "de", "it"]),
            "hashtags": [s.fake.word() for _ in range(random.randint(0, 5))],
            "mentions": [f"@{s.fake.user_name()}" for _ in range(random.randint(0, 3))],
        }
        return tweet

    # Generate a dataset of tweets
    def generate_dataset(s, topic, num_tweets):
        dataset = [s.generate_json(topic) for _ in range(num_tweets)]
        return dataset


if __name__ == "__main__":

    topics = ["artificial intelligence"]    #, "space exploration", "climate change"]

    gen = TweetGenerator()

    for topic in topics:
        tweet = gen.generate_text(topic)
        print("-" * 20, topic, "-" * 20)
        print(tweet)
    
    # for topic in topics:

    #     num_tweets = 1
    #     dataset = gen.generate_dataset(topic, num_tweets)
        
    #     # Save to file
    #     with open("data/tweets/" + topic + ".json", "w") as f:
    #         json.dump(dataset, f, indent=2)
    #         print(f"Generated {num_tweets} tweets and saved to {topic}'.json'")
        