# -*- coding: utf-8 -*-

"""
EtherscanLabelCrawler
EtherscanLabelCrawler An out-of-the-box ehterscan label crawler, you can use it to get all the labels info from etherscan.

Usage:
 etherscanlabel crawl <labelcategory> [--header=<file-path>]
 etherscanlabel -h | --help

Options:
  --header=<file-path>
  --help  -h show help info

Examples:
etherscanlabel crawl Binance --header /path/to/header.json  get binance related labels
etherscanlabel crawl all --header /path/to/header.json  get all labels in the label list


You must attach your header file, you can find an example file here: https://github.com/PixelHegel/Etherscan-Label-Crawler/blob/main/header_sample.json
"""

import json
import os
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup
from docopt import docopt
from tqdm import tqdm
import urllib3
import asyncio
import aiohttp
import logging
from aiohttp_retry import RetryClient, ExponentialRetry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#from etherscanlabel import __version__

cwd = os.getcwd()


def join(f):
    return os.path.join(os.path.dirname(__file__), f)


async def make_request(df,label_category_name,session, url,startrow,header, attempt=0):
    url = 'https://etherscan.io/accounts/label/{0}/?size=100&start={1}&col=1&order=asc'.format(label_category_name,startrow)
    async with session.get(url,headers=header) as response:
        if response.status == 200:
            try:
                data = await response.text()
                df_list = pd.read_html(data)
                df =  pd.concat([df,df_list[0]],ignore_index=True)
                if len(df)>=100:
                    new_startrow = len(df)
                    if len(df_list[0])==100:
                        return await make_request(df,label_category_name,session, url,new_startrow,header)
                return df
            except:
                pass

        #elif attempt < 3:
        #    print(f'failed #{attempt}')  # to debug, remove later
         #   return await make_request(df,label_category_name, session, url, startrow, header, attempt + 1)
        return None


async def start_crawler(label_category_name,header,pbar):
    df = pd.DataFrame()
    #timeout = aiohttp.ClientTimeout(total=3)
    async with aiohttp.ClientSession() as session:
        retry_options = ExponentialRetry(attempts=1, max_timeout=10)
        retry_client = RetryClient(client_session=session,retry_options=retry_options)
        label_category_name = label_category_name.rstrip().lower().replace(' ','-').replace('.','-')

        result = await make_request(df,label_category_name,retry_client,'',0,header)
        pbar.update(1)
        pbar.set_description("Fetching labels of %s" % label_category_name)
        return result


async def start_loop_crawler(label_list,header,pbar):
    async with aiohttp.ClientSession() as client:
        return await asyncio.gather(*[
            asyncio.ensure_future(start_crawler(label,header,pbar)) 
            for label in label_list
        ])


def init(args):

    if args["crawl"] and args["<labelcategory>"] !='all':
        label_category_name = args['<labelcategory>']
        if args['--header']:
            header_path = args['--header']
            f = open(header_path)
            header = json.load(f)
        else:
            print("You must attach your header file, you can find an example file here: https://github.com/PixelHegel/Etherscan-Label-Crawler/blob/main/header_sample.json")
            print(__doc__)
            exit(0)
        
        df_result = asyncio.run(start_crawler(label_category_name,header))


        if df_result is not None:
            path = cwd+'/{0}.csv'.format(label_category_name)
            df_result.to_csv(path)
            print('Your label data has saved into {0}'.format(path))
        else:
            print('Failed to crawl labels from etherscan, no file saved, please double check the category name')


    else:
        if args['--header']:
            header_path = args['--header']
            f = open(header_path)
            header = json.load(f)
        category_df = pd.read_csv(join("label_category_list.csv"))
        category_list = category_df['label_name']
        pbar = tqdm(total=len(category_list))
        loop = asyncio.new_event_loop()

        df_list = loop.run_until_complete(start_loop_crawler(category_list,header,pbar))
                
        asyncio.set_event_loop(loop)

        loop.close()
 
        df_result = pd.concat(df_list,ignore_index=True)
        pbar.close()
        if df_result is not None:
            path = cwd+'/all_labels.csv'
            df_result.to_csv(path)
            print('Your label data has saved into {0}'.format(path))
        else:
            print('Failed to crawl labels from etherscan, no file saved')


def main():
    args = docopt(__doc__)
    try:
        init(args)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
