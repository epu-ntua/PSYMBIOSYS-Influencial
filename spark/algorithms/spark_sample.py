__author__ = 'Michael'

import os
import sys

# Path for spark source folder
os.environ['SPARK_HOME']="C:\Syncfusion\BigDataSDK\2.1.0.77\SDK\Spark\bin"

# Append pyspark  to Python Path
sys.path.append("C:\Syncfusion\BigDataSDK\2.1.0.77\SDK\Spark\bin")

try:
    from pyspark import SparkContext
    from pyspark import SparkConf
    print ("Successfully imported Spark Modules")

except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)

# Initialize SparkContext
sc = SparkContext('local')
words = sc.parallelize(["scala","java","hadoop","spark","akka"])
print words.count()
