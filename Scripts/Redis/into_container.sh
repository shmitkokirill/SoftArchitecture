#!/bin/bash

echo "Output from the Redis"

if [ $1 = 'get_all' ]
then
    for key in $(redis-cli keys \*);
    do 
        echo "Key : '$key'" 
        redis-cli GET $key
    done
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
