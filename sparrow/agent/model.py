import os, config
from langchain_cohere.chat_models import ChatCohere

cohere_api_key1 = os.environ['COHERE_API_KEY1']
cohere_api_key2 = os.environ['COHERE_API_KEY2']
key_picker = 0

def pop_model():

    global key_picker
    if key_picker % 2 == 0:
        cohere_api_key = cohere_api_key1
    else:
        cohere_api_key = cohere_api_key2
    key_picker += 1
    print("key_picker", key_picker, cohere_api_key)
    return ChatCohere(model="command-r-plus", temperature=0, cohere_api_key=cohere_api_key)