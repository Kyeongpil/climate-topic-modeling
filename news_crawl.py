from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import os
import re
import newspaper
import sys
from time import sleep
from dateutil.relativedelta import relativedelta
from datetime import datetime
import ujson as json
from random import shuffle
from newspaper import Article
from multiprocessing import Process

headers = {'User-Agent': UserAgent()['Chrome']}

if not os.path.exists('./results'):
    os.mkdir('./results')


def crawl_one(urls, worker_id):
    articles = []
    urls = [[url, 0] for url in urls]
    max_trial = 10
    crawled_num = 0
    while True:
        all_finished = True
        print(f"===== {worker_id} iteration start =====")
        for i in range(len(urls)):
            url, trial = urls[i]
            if trial == -1:
                # already success
                continue

            try:
                article = Article(
                    url,
                    language='ko',
                    memorize_articles=False,
                    fetch_images=False,
                    skip_bad_cleaner=True,
                    headers=headers)
                article.download()
                sleep(0.1)
                j = 0
                while article.download_state != 2 and j < 10:
                    #ArticleDownloadState.SUCCESS is 2
                    sleep(0.5)
                    j += 1
                    raise newspaper.ArticleException
                
                article.parse()

                # 기사 정보 저장
                article_ = dict()
                article_['title'] = article.title.strip()
                article_['text'] = " ".join(article.text.split()).strip()
                article_['date'] = article.publish_date
                article_['url'] = url
                articles.append(article_)
                urls[i][1] = -1
                crawled_num += 1

                if crawled_num % 100 == 0:
                    print(
                        f"===== {worker_id} crawled - {crawled_num}/{len(urls)} =====")

            except BaseException as e:
                trial += 1
                urls[i][1] = trial
                print(f"{worker_id} - {type(e)}")
                if trial < max_trial:
                    all_finished = False

        if all_finished:
            break

    with open(f'./results/results_{worker_id}.json', 'w') as f:
        json.dump(articles, f)

    print(f"===== {worker_id} finished! =====")


if __name__ == '__main__':
    with open('urls.json') as f:
        urls = json.load(f)

    shuffle(urls)

    procs = []
    workers = 8
    chunk_size = len(urls)//workers
    for i in range(workers - 1):
        procs.append(Process(target=crawl_one, args=(
            urls[i*chunk_size: (i+1)*chunk_size], i,)))
    procs.append(Process(target=crawl_one, args=(
        urls[(i+1)*chunk_size:], i+1,)))

    for proc in procs:
        proc.start()

    try:
        for proc in procs:
            proc.join()
    except:
        for proc in procs:
            proc.terminate()

        sys.exit()
