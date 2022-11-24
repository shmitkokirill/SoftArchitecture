#!/bin/bash
CONTAINER="postgresql"

echo "Output from the $CONTAINER"

if [ $1 = 'autofill_tt' ]
then
    . /tmp/autofill_TT.sh $2
fi