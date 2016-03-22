__author__ = 'Michael'


from pyspark.mllib.stat import Statistics

api_mentions = sc.parallelize([ 23, 35, 56])
mpetyx_tweets = sc.parallelize([ 45, 67, 76])

corr = Statistics.corr(api_mentions, mpetyx_tweets, "pearson")
