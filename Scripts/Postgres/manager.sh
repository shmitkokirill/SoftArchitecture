#!/bin/bash

CONTAINER="postgresql"

docker cp ./into_container.sh $CONTAINER:/tmp/into_container.sh
docker cp ./autofill_TT.sh $CONTAINER:/tmp/autofill_TT.sh
docker cp ./autofill_Vis.sh $CONTAINER:/tmp/autofill_Vis.sh

docker exec $CONTAINER bash -c ". /tmp/into_container.sh $1 $2 $3" > ../../Output/$CONTAINER.out

if [ $( cat ../../Output/$CONTAINER.out | grep "$CONTAINER" | wc -l ) -eq 1 ]; then
  echo "The output file contains the expected output"
  echo
  cat ../../Output/$CONTAINER.out
else
  echo 'The output file does not contain the expected output'
fi