#!/bin/bash

students_ids_string=$(export PGPASSWORD='111'; psql -h localhost -p 5432 \
            -U 'kirill' \
            -d 'university' \
            -c "select code from Students;")
readarray -t y <<< "$students_ids_string"
unset y[0]
unset y[1]
unset y[-1]
st_ids=("${y[@]}"); #array

students_nms_string=$(export PGPASSWORD='111'; psql -h localhost -p 5432 \
            -U 'kirill' \
            -d 'university' \
            -c "select FULLNAME from Students;")
readarray -t y <<< "$students_nms_string"
unset y[0]
unset y[1]
unset y[-1]
st_nms=("${y[@]}"); #array

for (( i=0; i<${#st_nms[@]}; i++ ));
do 
    code="$(echo -e "${st_ids[$i]}" | tr -d '[:space:]')"  # trim
    name="$(echo -e "${st_nms[$i]}" | tr -d '[:space:]')"  # trim
    redis-cli set "$code" "$name"
done