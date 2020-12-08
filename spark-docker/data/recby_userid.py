#!/usr/bin/python
#  -*- coding: utf-8 -*-
import argparse
from pymongo import MongoClient as MC

parser = argparse.ArgumentParser()
parser.add_argument('--userid', type=int, default='8')
args = parser.parse_args()

client = MC('124.70.27.99', 27017)
db = client.admin
db.authenticate("admin", "123456", mechanism='SCRAM-SHA-1')

userRec = db.userRec
result = userRec.find_one({'userid': args.userid})

movies = result['recbooks']
movies.sort(key=lambda x: float(x['rate']), reverse=True)

with open('/tmp/data/output/usr_' + str(args.userid) + '_rec.txt', 'w') as f:
    f.write('针对用户 %s 进行推荐：\n' % str(args.userid))
    for movie in movies:
        f.write('%d. 推荐：%s, 推荐指数为: %.2f，在源数据中id为：%s\n' % (
        movies.index(movie)+1, movie['itemname'], float(movie['rate']), movie['itemid']))
