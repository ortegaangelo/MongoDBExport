# MongoDBExport
Export from MongoDB as CSV + Upload on SFTP
This project contains 3 possible solutions in python (app.py) to export data from mongo db and upload them to a sftp server.
**Experimental** I am not a python expert :)

## Solution 1 
Connects to MongoDB and exports a single collection, with all its fields to a csv, via [pymongo](https://pypi.python.org/pypi/pymongo).

## Solution 2
Using the command [mongoexport](https://docs.mongodb.com/manual/reference/program/mongoexport/) to export a set of fields from MongoDB into a csv.

## Solution 3
Using a bash script to call the commands [mongo](https://docs.mongodb.com/manual/reference/program/mongo/) & [mongoexport](https://docs.mongodb.com/manual/reference/program/mongoexport/) and export ALL collections with ALL fields from MongoDB into a csv. This script can also be used directly from the command line.
