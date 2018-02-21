import time
import pysftp
import os
import glob
import subprocess
from pymongo import MongoClient

class App:
    sftp_host = 'www.somewhere.de'
    sftp_user = 'sftpuser'
    sftp_pw = 'password'
    sftp_path = '/uploads/'

    mongo_host = "mongodb.host.com"
    mongo_user = "mongouser"
    mongo_pw = "password"
    mongo_port = 43418
    mongo_db = 'heroku_db'
    mongo_collection = 'Collection1'

    def __init__(self):
        file_names = self.solution_one()  # Connect to Mongo DB and export a single collection via pymongo
        file_names = self.solution_two()  # Use Mongoexport from python to export a set of fields from a collection
        file_names = self.solution_three()  # Use custom script to export ALL collections

        # Send to sftp
        for file_name in file_names:
            self._send_to_sftp(self.sftp_host, self.sftp_user, self.sftp_pw, file_name, self.sftp_path)
            os.remove(file_name) # Delete after send to ftp

    def solution_one(self):
        # Connect to mongodb collection
        cs = "mongodb://{}:{}@{}/{}".format(self.mongo_user,self.mongo_pw,self.mongo_host,self.mongo_db)
        db = self._connect(cs, self.mongo_port)
        collection = db[self.mongo_db][self.mongo_collection]

        # Generate file/name
        time_str = time.strftime("%Y%m%d-%H%M%S")
        file_name = "{}_{}.csv".format(self.mongo_collection, time_str)
        file = open(file_name, 'w')
        keys = None

        # Read the collection and write to file
        for document in collection.find():
            # Write header once
            if keys is None:
                keys = document.keys()
                keystr = ','.join(keys)
                file.write(keystr)

            # Get line
            lines = []
            for key in keys:
                lines.append(str(document[key]))
            line_str = ','.join(lines)
            file.write('\n')
            file.write(line_str)
        file.close()

        return [file_name]

    def solution_two(self):
        # Fields
        fields = ['id', 'company']
        # Generate file/name
        time_str = time.strftime("%Y%m%d-%H%M%S")
        file_name = "{}_{}.csv".format(self.mongo_collection, time_str)

        # The connection string
        cs = "mongodb://{}:{}@{}/{}".format(self.mongo_user, self.mongo_pw, self.mongo_host, self.mongo_db)

        # The mongoexport cmd line call
        output = subprocess\
            .check_output((["mongoexport",
                           "--host={}:{}".format(self.mongo_host, self.mongo_port),
                           "--db={}".format(self.mongo_db),
                           "--username={}".format(self.mongo_user),
                           "--password={}".format(self.mongo_pw),
                           "--collection={}".format(self.mongo_collection),
                           "--type=csv",
                           "--fields={}".format(','.join(fields)),
                           "--out={}".format(file_name)]))

        print output
        return [file_name]

    def solution_three(self):
        print subprocess.check_output(["./export-all-csv-mongo.sh", self.mongo_db, self.mongo_user, self.mongo_pw,
                                       "{}:{}".format(self.mongo_host, self.mongo_port)])

        results = [i for i in glob.glob("export.*.csv")]
        print results
        for file_name in results:
            self._send_to_sftp(self.sftp_host, self.sftp_user, self.sftp_pw, file_name, self.sftp_path)

        return results

    def _connect(self, address, port, lazy_connection=False):
        client = MongoClient(address, port)
        if lazy_connection:
            return client

        # Check if connection works
        try:
            client.server_info()
        except Exception as exc:
            print exc.message
            client = None

        return client

    def _send_to_sftp(self, host, username, password, file, target_path):
        with pysftp.Connection(host, username=username, password=password) as sftp:
            sftp.put(file, target_path+file)
        print 'Upload done.'

App()
