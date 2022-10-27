#!/bin/bash
docker cp ./into_container.sh redis:/tmp/into_container.sh
docker cp ./autofill.sh redis:/tmp/autofill.sh

docker exec redis bash -c ". /tmp/into_container.sh $1 $2 $3" > ../../Output/redis.out

if [ $( cat ../../Output/redis.out | grep "Redis" | wc -l ) -eq 1 ]; then
  echo "The output file contains the expected output"
  echo
  cat ../../Output/redis.out
else
  echo 'The output file does not contain the expected output'
fi