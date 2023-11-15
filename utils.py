import string
import re
import yfinance as yf
import openai
import boto3

from config import *

def remove_punctuation(word):
    punc_remove_list = [
        char for char in word if char not in string.punctuation]
    punc_removed_word = ''.join(punc_remove_list)
    return punc_removed_word


def remove_emoji(word):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', word)


def contains_number(word):
    for char in word:
        if char.isdigit():
            return True
    return False


def validate_ticker(log, ticker):
    print(f'in validate_ticker for ticker:: {ticker}')
    log.info(f'in validate_ticker for ticker: {ticker}')

    yahoo_data = yf.download(tickers=ticker, interval='1d')

    print(f'yahoo_data: {yahoo_data}')
    log.info(f'yahoo_data: {yahoo_data}')

    if not yahoo_data.empty:
        # get the current price
        current_price = round(yahoo_data['Close'].iloc[-1], 2)
        return True, current_price

    return False, None


def get_gpt_summary(log,prompt):
    openai.api_key = GPT_SECRET_KEY
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            prompt
            ]
    ).choices[0].message.content.strip()
    
    log.info(f'Here is the gpt response: {response}')
    return response

'''
#openai.error.invalidrequesterror: this model's maximum context length is 4097 tokens, however you requested 4969 tokens (4953 in your prompt; 16 for the completion). please reduce your prompt; or completion length.
def get_gpt_summary(log, prompt):
    log.info(f'In get_gpt_summary with prompt: {prompt}')

    openai.api_key = GPT_SECRET_KEY
    completion = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        temperature=0
    ).choices[0].text.strip()

    log.info(f'Here is the gpt response: {completion}')
    return completion
'''

def upload_log_to_aws(log, log_file):
    log.info('in upload_log_to_aws')

    s3_client = boto3.client(
        service_name='s3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    response = s3_client.upload_file(log_file, AWS_S3_BUCKET_NAME, log_file)

    log.info(f'upload_log_to_aws response: {response}')