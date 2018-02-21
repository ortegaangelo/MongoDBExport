# MongoDBExport
Export from MongoDB as CSV + Upload on SFTP
This project contains 3 possible solutions in python (app.py) to export data from mongo db and upload them to a sftp server.
**Experimental** I am not a python expert :)

## Solution 1 
Connects to MongoDB and exports a single collection, with all its fields to a csv, via pymongo.

## Solution 2
Using the command mongoexport (cmd) to export a set of fields from MongoDB into a csv.

## Solution 3
Using a bash script to call the commands mongo & mongoexport and export ALL collections with ALL fields from MongoDB into a csv. This script can also be used directly from the command line.
