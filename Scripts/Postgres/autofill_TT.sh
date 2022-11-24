#!/bin/bash
# export PGPASSWORD='111'; psql -h '172.17.0.2' -U 'kirill' -d 'university' -c "$1"

get_lec_time() {
    case $1 in
        0) echo "09:00" ;;
        1) echo "10:40" ;;
        2) echo "12:40" ;;
        3) echo "14:20" ;;
        4) echo "16:20" ;;
        5) echo "18:00" ;; 
        *) echo "09:00" ;;
    esac
}

# get group cods from Group -table
g_cods_str=$(export PGPASSWORD='111'; psql -h '172.17.0.2' -U 'kirill' \
    -d 'university' -c 'select code from Groups;')
readarray -t y <<< "$g_cods_str"
unset y[0]
unset y[1]
unset y[-1]
g_cods=("${y[@]}");

# get lesson's id's 
les_ids_str=$(export PGPASSWORD='111'; psql -h '172.17.0.2' -U 'kirill' \
    -d 'university' -c 'select id from Lesson;')
readarray -t y <<< "$les_ids_str"
unset y[0]
unset y[1]
unset y[-1]
les_ids=("${y[@]}");

# autofill table "Timetable"; input - count of days
build_timetable_per_days() {
    for (( j=0; j < $1; j++ ));
    do
        les_count=$((1 + $RANDOM % 6));
        dt=$(date -d "2022-11-01 $j days" +%Y-%m-%d);
        for (( i=0; i < $les_count; i++ ));
        do
            tm=$(get_lec_time $i);
            indx_les=$(($RANDOM % ${#les_ids[@]}));
            les_id=${les_ids[$indx_les]};
            indx_g=$(($RANDOM % ${#g_cods[@]}))
            g_code="$(echo -e "${g_cods[$indx_g]}" | tr -d '[:space:]')"  # trim 
            date_time="$dt $tm";
            export PGPASSWORD='111'; psql -h '172.17.0.2' -U 'kirill' \
                -d 'university' \
                -c "INSERT INTO Timetable(date, groupId, lessonId, lessonNum) 
                    VALUES ('$date_time', '$g_code', $les_id, (($i + 1)));"
        done
    done
}

build_timetable_per_days $1

# fill in VISIT -table
. /tmp/autofill_Vis.sh