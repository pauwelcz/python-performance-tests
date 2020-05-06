import select
import datetime
import csv

import psycopg2
import psycopg2.extensions

import functions
import timeit
import time

csvList = []
csvList.append(["Benchmark", "Mode", "Threads", "Score", "Unit", "noProcesses", "numInserts"])

fiveHundred = open("./data/five_hundred.txt", "r").read()
threeHundredThousand = open("./data/three_hundred_thousand.txt", "r").read()
binaryImage = open("./data/postgresql-logo.png", "rb").read()
# connect into database
connection_string = "host='localhost' dbname='postgres' user='xsedla0k' password='bejbojsu8m'"
connection = psycopg2.connect(connection_string)
cursor = connection.cursor()
functions.listen(cursor)

functions.delete(cursor, connection)
# insert_text_message, id++, default_message
print("Performance tests:")
print("\tinsertNaive")

sumTimingResult = timeit.repeat(
    globals = globals(),  # access the global variables in this scope
    stmt = 'functions.insertNaive(cursor, connection); functions.notify(connection);',
    number = 1000,
    repeat = 1
)

csvList.append(["insertNaive", "avgt", 1, functions.getScore(sumTimingResult, 1000), "s/op", 0, 0])


functions.delete(cursor, connection)
# insert_text_message, id++, default_message
print("\tinsertHundredsOfChars")
sumTimingResult = timeit.repeat(
    globals = globals(),  # access the global variables in this scope
    stmt = 'functions.insert(cursor, connection, fiveHundred); functions.notify(connection);',
    number = 1000,
    repeat = 1
)


csvList.append(["insertHundredsOfChars", "avgt", 1, functions.getScore(sumTimingResult, 1000), "s/op", 0, 0])

functions.delete(cursor, connection)
# insert_text_message, id++, default_message
print("\tinsertHundredsOfThousandsOfChars")

sumTimingResult = timeit.repeat(
    globals = globals(),  # access the global variables in this scope
    stmt = 'functions.insert(cursor, connection, threeHundredThousand); functions.notify(connection);',
    number = 1000,
    repeat = 1
)

csvList.append(["insertHundredsOfThousandsOfChars", "avgt", 1, functions.getScore(sumTimingResult, 1000), "s/op", 0, 0])


print("\tinsertTextAndImage")
sumTimingResult = timeit.repeat(
    globals = globals(),  # access the global variables in this scope
    stmt = 'insert_id = functions.insertNaive(cursor, connection);functions.notify(connection);functions.insertBin(cursor, connection, binaryImage, insert_id);functions.notify(connection);',
    number = 1000,
    repeat = 1
)
csvList.append(["insertTextAndImage", "avgt", 1, functions.getScore(sumTimingResult, 1000), "s/op", 0, 0])

print("\tinsertTextAndImageAndDelete")
sumTimingResult = timeit.repeat(
    globals = globals(),  # access the global variables in this scope
    stmt = 'insert_id = functions.insertNaive(cursor, connection); functions.notify(connection);   functions.insertBin(cursor, connection, binaryImage, insert_id);  functions.notify(connection); functions.deleteFromTable(cursor, connection, insert_id); functions.notify(connection);',
    number = 1000,
    repeat = 1
)
csvList.append(["insertTextAndImageAndDelete", "avgt", 1, functions.getScore(sumTimingResult, 1000), "s/op", 0, 0])


print("Performance tests completed")
#adding to csvFile
with open('./output/results_python_single.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for i in csvList:
        wr.writerow(i)
