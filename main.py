import logging
import os
import datetime
import json

from config import *
from reddit import get_reddit_tickers_and_comments
from utils import validate_ticker, get_gpt_summary, upload_log_to_aws
from sendEmail import send_email


log = logging.getLogger()

def logging_handler():
    print("In logging_handler")

    log_directory = SENTIMENTAL_NEWSLETTER_LOG_PATH

    #Making a directoy-if not exists 
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_format = '%(asctime)s %(levelname)s %(module)s:%(lineno)d %(message)s'

    #set up constant stream of logs so logs are written as they are hit in the script
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(stream_handler)

    #set up logs to write to a specific file in a specific folder
    log_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f'{log_directory}log-{log_name}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)

    logging.getLogger().setLevel(logging.DEBUG)

    return log_file


def main():
    print('In main method')

    log_file = logging_handler()

    log.info(f"Started script at {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")

    reddit_tickers = get_reddit_tickers_and_comments(log)
    log.info(f"Here is the reddit_tickers in main: {json.dumps(reddit_tickers, indent=4)}")

    final_comments_ticker_dicts = reddit_tickers.copy()

    final_comments_ticker_dicts = [  item for item in final_comments_ticker_dicts if item['comment_count'] >= GPT_MIN_COMMENT_COUNT ]
    #log.info(f"Here is the final_comments_ticker_dicts in main: {json.dumps(final_comments_ticker_dicts, indent=4)}")
    log.info(f"Here is the final_comments_ticker_dicts in main: {final_comments_ticker_dicts}")

    summary_list = [] 
    
    for ticker_dict in final_comments_ticker_dicts:
        is_valid, current_price = validate_ticker(log, ticker_dict['ticker'])

        if is_valid:
            log.info(f"ticker {ticker_dict['ticker']} is valid, sending to GPT for summary")
            
            #put all of the comments into one sentence
            comment_sentence = " ,".join(ticker_dict['comments'])
            log.info(f"Here is the comment_sentence in main: {json.dumps(comment_sentence, indent=4)}")
            #This model's maximum context length is 4097 tokens
            prompt = f"Can you give short summarize what people are saying about {ticker_dict['ticker']} in these comments: '{comment_sentence}'"
            log.info(f'Here is the prompt: {prompt}')

            gpt_response = get_gpt_summary(log, {"role": "user", "content": prompt})
            log.info(f'Here is the gpt_response in main: {gpt_response}')
            
            if gpt_response is not None:
                summary_dict = {}
                summary_dict['ticker'] = ticker_dict['ticker']
                summary_dict['gpt_summary'] = gpt_response
                summary_dict['current_price'] = current_price
                summary_list.append(summary_dict)
                
    #if the summary_list is not null then send email
    log.info(f'Here is the final summary list: {json.dumps(summary_list, indent=4)}')

    send_email(log, summary_list)
    
    upload_log_to_aws(log, log_file)     


if __name__ == '__main__':
    main()