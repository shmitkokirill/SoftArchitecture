#!/bin/bash

# $1 - min date
host='172.17.0.1'

date_min=$(date -d "$1" +%Y-%m-%d);
for (( j=0; j < 6; j++ ));
do
    date_max=$(date -d "$date_min + 7 days" +%Y-%m-%d);
    export PGPASSWORD='111'; psql -h $host -U 'kirill' \
                -d 'university' \
                -c "CREATE TABLE visit_$j ( like VISIT including all );
                    ALTER TABLE visit_$j inherit VISIT;
                    ALTER TABLE visit_$j add constraint partitioning_check check 
                        ( date >= '$date_min'::DATE AND date < '$date_max'::DATE);"
    date_min=$date_max;
done

. /tmp/trigger_partition.sh $1