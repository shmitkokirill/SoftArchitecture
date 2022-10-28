#!/bin/bash
docker cp ./into_container.sh mongo:/tmp/into_container.sh
# docker cp ./autofill.sh mongo:/tmp/autofill.sh

docker exec mongo bash -c ". /tmp/into_container.sh $1 $2 $3" > ../../Output/mongo.out

if [ $( cat ../../Output/mongo.out | grep "Mongo" | wc -l ) -eq 1 ]; then
  echo "The output file contains the expected output"
  echo
  cat ../../Output/mongo.out
else
  echo 'The output file does not contain the expected output'
fi