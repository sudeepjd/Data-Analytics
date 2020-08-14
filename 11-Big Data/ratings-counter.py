#Data Source : https://grouplens.org/datasets/movielens/

from pyspark import SparkConf, SparkContext
import collections

conf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc = SparkContext(conf = conf)

lines = sc.textFile("ratings.csv")
print(lines.top(2))

ratings = lines.map(lambda x: x.split(",")[2])
print(ratings.top(2))

result = ratings.countByValue()

sortedResults = collections.OrderedDict(sorted(result.items()))
for key, value in sortedResults.items():
    print("%s %i" % (key, value))