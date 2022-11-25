#!/bin/bash

les_ids_string=$(export PGPASSWORD='111'; psql -h localhost -p 5432 \
            -U 'kirill' \
            -d 'university' \
            -c "select lessonid from Timetable;")
readarray -t y <<< "$les_ids_string"
unset y[0]
unset y[1]
unset y[-1]
les_ids=("${y[@]}"); #array

dates_string=$(export PGPASSWORD='111'; psql -h localhost -p 5432 \
            -U 'kirill' \
            -d 'university' \
            -c "select date from Timetable;")
readarray -t y <<< "$dates_string"
unset y[0]
unset y[1]
unset y[-1]
dates=("${y[@]}"); #array

for (( i=0; i<${#dates[@]}; i++ ));
do 
    d="$(echo -e "${dates[$i]}" | tr -d '[:space:]')"  # trim wrong!!!
    les_id="$(echo -e "${les_ids[$i]}" | tr -d '[:space:]')"  # trim
    curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
        -H "Accept: application/json" -H 'Content-type: application/json' \
        -d '{"statements": [{"statement": "CREATE (l:Lesson{date:\"'"$d"'\", id:\"'"$les_id"'\"});"}]}' \
        -o log.out
done
