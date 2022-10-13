# -*- coding: utf-8 -*-

"""
EtherscanLabelCrawler
EtherscanLabelCrawler An out-of-the-box ehterscan label crawler, you can use it to get all the labels info from etherscan.

Usage:
 etherscanlabel crawl <labelcategory> [--header <file-path>]
 etherscanlabel -h | --help

Options:
  --header <file-path>  your header info
  --help  -h show help info

Examples:
etherscanlabel crawl Binance --header /path/to/header.json
"""

from docopt import docopt
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
import os
import json
from tqdm import tqdm

cwd = os.getcwd()


def join(f):
    return os.path.join(os.path.dirname(__file__), f)

def get_labels_from_category(label_category_name,df,startrow,header):

    label_category_name = label_category_name.rstrip().lower().replace(' ','-').replace('.','-')
    url = 'https://etherscan.io/accounts/label/{0}/?size=25&start={1}'.format(label_category_name,startrow)
    try:
        response = requests.get(url=url, headers=header)

        df_list = pd.read_html(response.content)
        df = pd.concat([df,df_list[0]],ignore_index=True)
        if len(df)>=25:
            new_startrow = len(df)
            if len(df_list[0])>=25:
                return get_labels_from_category(label_category_name,df,new_startrow,header)
        return df


    except Exception as e: 
        #TODO
        pass


def init(args):
    if args["crawl"] and args["<labelcategory>"] !='all':
        label_category_name = args['<labelcategory>']
        header_path = args['--header']
        f = open(header_path)
        data = json.load(f)

        df = pd.DataFrame()
        df_result = get_labels_from_category(label_category_name,df,0,data)
        path = cwd+'/{0}.csv'.format(label_category_name)
        df_result.to_csv(path)
        print('Your label data has saved into {0}'.format(path))

    else:
        category_df = pd.read_csv(join("label_category_list.csv")).head(10)
        category_list = category_df['label_name']
        df_list = []
        pbar = tqdm(category_list)
        for label_category_name in pbar:
            header_path = args['--header']
            f = open(header_path)
            data = json.load(f)
            try:
                df_temp = pd.DataFrame()
                df_temp = get_labels_from_category(label_category_name,df_temp,0,data)
                if df_temp is not None:
                    df_temp['category']=label_category_name
                    df_list.append(df_temp)

                df_result = pd.concat(df_list,ignore_index=True)
            except Exception as e: 
                print(e)
                continue
            pbar.set_description("Fetching labels of %s" % label_category_name)
            sleep(1.1)
        
        if df_result is not None:
            path = cwd+'/all_labels.csv'
            df_result.to_csv(path)
            print('Your label data has saved into {0}'.format(path))



def main():
    args = docopt(__doc__)
    try:
        init(args)
    except KeyboardInterrupt:
        sys.exit(0)



if __name__ == '__main__':
    main()
