#!/bin/bash

echo "Output from the Mongo"

if [ $1 = 'get_all' ]
then
    echo "db.getMongo().getDBNames()"|mongo --quiet |tr -d \[\] | tr , "\n"|cut -c3-| tr -d \"
elif [ $1 = 'set' ]
then
    redis-cli set $2 $3
elif [ $1 = 'get' ]
then
    redis-cli get $2
elif [ $1 = 'del' ]
then
    redis-cli del $2
elif [ $1 = 'flush' ]
then
    redis-cli flushall
elif [ $1 = 'autofill' ]
then
    . /tmp/autofill.sh $2 
fi
