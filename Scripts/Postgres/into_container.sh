#!/bin/bash
CONTAINER="postgresql"

echo "Output from the $CONTAINER"

if [ $1 = 'autofill_tt' ]
then
    . /tmp/autofill_TT.sh $2 $3
elif [ $1 = 'partition' ]
then
    . /tmp/create_partitions.sh $2
fi