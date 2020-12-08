#!/usr/bin/python
#  -*- coding: utf-8 -*-
import time
import json
import requests
import random


def EmotAna(sent="I love it, I used this for my Yamaha ypt-230 and it works great, I would recommend it to anyone"):
    # 获得access_token
    AK = "f07s15cyySl9ZvCnwfLGFeMk"
    SK = "5C5VuRGnaX1zjmiAp9H4CNdxUrsN0S1g"
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(
        AK, SK)
    res = requests.post(host)
    Token1 = json.loads(res.text)
    Token = Token1['access_token']

    # 获得分析文本
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token={}'.format(Token)
    data = {
        'text': sent,
    }
    data = json.dumps(data)
    res2 = requests.post(url, data=data)
    # 取出正向情感倾向
    res3 = json.loads(res2.text)
    pos_prob = res3["items"][0]["positive_prob"]

    # print(pos_prob)
    # if pos_prob<0.7 and pos_prob>0.3:
    #     rate = 0.5
    # else:
    rate = pos_prob

    return rate


# 为u.data添加非格式化评论文本
def process1_add():
    source1 = r"Musical_Instruments_5.json"
    source2 = r"u_old.data"
    outputfile = "u.data"
    # 读取u_old文件至列表
    with open(source2, 'r', encoding='ISO-8859-1') as f:
        datalines = f.readlines()
    datalines = [e.split("\t") for e in datalines]

    # 读取评论列表
    revTexts = []
    with open(source1, 'r', encoding='utf8') as f:
        for jsonstr in f.readlines():
            data = json.loads(jsonstr)
            text = data['reviewText']
            revTexts.append(text)
    print(len(revTexts))

    for i in range(len(datalines)):
        datalines[i][3] = random.choice(revTexts)

    with open(outputfile, 'w', encoding='ISO-8859-1') as f:
        for e in datalines:
            f.write(e[0] + '\t' + e[1] + '\t' + e[2] + '\t' + e[3] + '\n')


# 情感分析加权得到u_proc.data
def proces2_ana():
    source1 = "u.data"
    outputfile = "u_proc.data"
    # 读取u_old文件至列表
    with open(source1, 'r', encoding='ISO-8859-1') as f:
        datalines = f.readlines()
    datalines = [e.split("\t") for e in datalines]

    data_results = []
    for e in datalines:
        emorate = EmotAna(e[3])
        # 加偏移修正，防止打分接近0
        emorate2 = 1.0 + float(e[2]) * emorate * 4.0 / 5
        print(emorate, emorate2)
        data_results.append([e[0], e[1], emorate2])
        time.sleep(0.55)
        # print(e[0], e[1], emorate2)

    with open(outputfile, 'w', encoding='ISO-8859-1') as f:
        for e in data_results:
            f.write(e[0] + '\t' + e[1] + '\t' + str(round(e[2], 2)) + '\n')

    return

# EmotAna()
# process1_add()
# proces2_ana()
