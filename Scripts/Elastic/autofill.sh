#!/bin/bash

# get tt ids from Timetable -table
tit_les_str=$(export PGPASSWORD='111'; psql -h '172.17.0.5' -U 'kirill' \
    -d 'university' \
    -c "select title from lesson;")
readarray -t y <<< "$tit_les_str"
unset y[0]
unset y[1]
unset y[-1]
tits=("${y[@]}"); #array
# get tt ids from Timetable -table
id_les_str=$(export PGPASSWORD='111'; psql -h '172.17.0.5' -U 'kirill' \
    -d 'university' \
    -c "select id from lesson;")
readarray -t y <<< "$id_les_str"
unset y[0]
unset y[1]
unset y[-1]
les_ids=("${y[@]}"); #array

for (( j=0; j < ${#les_ids[@]}; j++ ));
do
    les_id="$(echo -e "${les_ids[$j]}" | tr -d '[:space:]')"  # trim
    title=${tits[$j]};
    curl -u elastic:111111 -X PUT "http://localhost:9200/lessons/_doc/$j?pretty" \
    -H 'Content-Type: application/json' -d "{\"id\":\"$les_id\",\"title\":\"$title\",\"material\":\"empty\"}"
done

# for (( j=1; j < ${#les_ids[@]}; j++ ));
# do
#     curl -u elastic:111111 -X DELETE "http://localhost:9200/lessons/_doc/$j?pretty"
# done