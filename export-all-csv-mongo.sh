#!/bin/bash

OIFS=$IFS;
IFS=",()][";

# fill in your details here
dbname=$1
user=$2
pass=$3
host=$4

# first get all collections in the database
collections=`mongo "$host/$dbname" -u $user -p $pass --eval "rs.slaveOk();db.getCollectionNames();"`;
collectionArray=(${collections});

# for each collection
for ((i=0; i<${#collectionArray[@]}; ++i));
do
    collection=${collectionArray[i]}
    collection=${collection//\"}
    collection=$(echo -e ${collection} | tr -d '[:space:]')

    #sed -e 's/^"//' -e 's/"$//' <<<"$collection"

    echo 'exporting collection' ${collection}
    # get comma separated list of keys. do this by peeking into the first document in the collection and get his set of keys
    keys=`mongo "$host/$dbname" -u $user -p $pass --eval "rs.slaveOk();var keys = []; for(var key in db.${collection}.find().sort({_id: -1}).limit(1)[0]) { keys.push(key); }; keys;" --quiet`;
    keysArray=(${keys})

    IFS="][";
    keystr=$(printf ",%s" "${keysArray[@]//\"}")
    keystr=${keystr:1}
    keystr=$(echo -e ${keystr} | tr -d '[:space:]')

    echo 'keys:' ${keystr}
    mongoexport --host $host -u $user -p $pass -d $dbname -c $collection --fields ${keystr} --type csv --out export.${dbname}.${collection}.csv;
done

IFS=$OIFS;
