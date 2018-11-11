from glob import glob
from konlpy.tag import Okt
import re
import ujson as json
import pickle
twitter = Okt()
tag_set = set(['Noun', 'Verb', 'Adjective'])


filenames = glob('./results/results*.json')
data = []

for filename in filenames:
    with open(filename) as f:
        d = json.load(f)
        for article in d:
            if article['title'] != '' and article['text'] != '' and article['date'] is not None:
                data.append(article)
                
                
print(len(data))


def regexp(str_):
    str_ = re.sub(r'【.+】', ' ', str_)
    str_ = re.sub(r'\[\w+=(\w+)?( )?\w+]', ' ', str_)
    str_ = re.sub(r'\(\w+( )?=( )?(\w+)\w+\)', ' ', str_)
    str_ = re.sub(r'<\S+=\S+>', ' ', str_)
    str_ = re.sub(r'원본 기사 보기', ' ', str_)
    str_ = re.sub(r'구독신청', ' ', str_)
    str_ = re.sub(r'출처( )?=( )?\w+ 제공', ' ', str_)
    str_ = re.sub(r'\w+( )?제공', ' ', str_)
    str_ = re.sub(r'기사제보 및 보도자료', ' ', str_)
    str_ = re.sub(r'무단( )?전재 및 재배포 금지', ' ', str_)
    str_ = re.sub(r'송고( )?(시간)?', ' ', str_)
    str_ = re.sub(r'(저작권자 )?© (\w+)?', ' ', str_)
    str_ = re.sub(r'\w+ 바로가기', ' ', str_)
    str_ = re.sub(r'\w+( )?(\S+)?( )?기자', ' ', str_)
    str_ = re.sub(r'\(\w+\)', ' ', str_)
    str_ = re.sub(r'\w+(일보|닷컴|신문|뉴스)', ' ', str_)
    str_ = re.sub(r'(페이스북메신저|밴드|블로그|구글플러스|핀터레스트)', ' ', str_)
    str_ = " ".join(str_.split())    
    return str_

results = []
for i, article in enumerate(data):
    if i % 1000 == 0:
        print(i)

    re_text = regexp(article['text'])
    if len(re_text) > 0:        
        words = twitter.pos(re_text, norm=True, stem=True)
        words = [w for w, t in words if t in tag_set]
        article['tokens'] = words
        results.append(article)
    
with open('words_preprocessed.json', 'w') as f:
    json.dump(results, f)
