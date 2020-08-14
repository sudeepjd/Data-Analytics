from pyspark.sql import SparkSession
from pyspark.sql import Row

import collections

# Create a SparkSession (Note, the config section is only for Windows!)
spark = SparkSession.builder.master("local[*]").config("spark.sql.warehouse.dir", "file:///C:/temp").appName("SparkSQL").getOrCreate()

#Use a function to split up the Data into Rows on the DataFrame
def mapper(line):
	fields = line.split(',')
	return Row(userID=fields[0], movieID=fields[1], rating=fields[2], timestamp=fields[3])

lines = spark.sparkContext.textFile("ratings.csv")
ratings = lines.map(mapper)

# Infer the schema, and register the DataFrame as a table.
schemaRatings = spark.createDataFrame(ratings).cache()
schemaRatings.createOrReplaceTempView("ratings")
schemaRatings.show()

# SQL can be run over DataFrames that have been registered as a table.
rating4 = spark.sql("SELECT rating, COUNT(*) FROM ratings GROUP BY rating")
rating4.show()

# The results of SQL queries are RDDs and support all the normal RDD operations.
for rate in rating4.collect():
  print(rate)

# We can also use functions instead of SQL queries:
schemaRatings.groupBy("rating").count().orderBy("rating").show()
schemaRatings.select(schemaRatings["movieID"], schemaRatings["rating"]).groupBy(schemaRatings["movieID"], schemaRatings["rating"]).count().show()

#Stop the session
spark.stop()
