#!/usr/bin/python
#  -*- coding: utf-8 -*-
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkSessionExample") \
    .master("spark://master:7077") \
    .config("spark.some.config.option", "some-value") \
    .config('spark.debug.maxToStringFields', '50') \
    .getOrCreate()
# 获取SparkContext实例对象
sc = spark.sparkContext
# 获取推荐数据
rdd = sc.textFile("/tmp/data/ml-100k/u_pro.data")

# 转换RDD格式

rawRatings = rdd.map(lambda line: line.split("\t")[:3])
ratingsRDD = rawRatings.map(lambda x: (x[0], x[1], x[2]))
# 测试输出数据
ratingsRDD.take(5)
# 构建itemid2name数据
itemRDD = sc.textFile("/tmp/data/ml-100k/u.item")
itemid2name = itemRDD.map(lambda line: line.split("|")).map(lambda a: (float(a[0]), a[1])).collectAsMap()
# 训练
from pyspark.mllib.recommendation import ALS
model = ALS.train(ratingsRDD, 10, 10, 0.01)
# 链接mongodb数据库
from pymongo import MongoClient as MC
client = MC('124.70.27.99', 27017)
db = client.admin
db.authenticate("admin", "123456", mechanism='SCRAM-SHA-1')
userRec = db.userRec
# 构建用户列表
useridlist = range(1, 944)
for userid in useridlist:
    if userid%50==0:
        print('rec userid', userid)
    recp = model.recommendProducts(int(userid), 10)
    userrecinfo = {'userid': userid,'recbooks': [{'itemid': str(p[1]), 'itemname': itemid2name[p[1]], 'rate': str(p[2])} for p in recp]}
    # 写入mongoDB数据库
    userRec.insert_one(userrecinfo)


