#!/bin/bash

get_isVisited() {
    case $1 in
        0) echo "true" ;;
        1) echo "false" ;;
        *) echo "false" ;;
    esac
}

# get stud cods from GroupStudent -table
st_cods_str=$(export PGPASSWORD='111'; psql -h '172.17.0.2' -U 'kirill' \
    -d 'university' -c 'select code_st from GroupStudent;')
readarray -t y <<< "$st_cods_str"
unset y[0]
unset y[1]
unset y[-1]
st_cods=("${y[@]}"); #array

# get group cods from GroupStudent -table
g_cods_str=$(export PGPASSWORD='111'; psql -h '172.17.0.2' -U 'kirill' \
    -d 'university' -c 'select code_group from GroupStudent;')
readarray -t y <<< "$g_cods_str"
unset y[0]
unset y[1]
unset y[-1]
g_cods=("${y[@]}"); #array

# autofill table "Visit"
build_visit() {
    # give a student...
    for (( i=0; i < ${#g_cods[@]}; i++ ));
    do
        g_code="$(echo -e "${g_cods[$i]}" | tr -d '[:space:]')"  # trim
        st_code="$(echo -e "${st_cods[$i]}" | tr -d '[:space:]')"  # trim

        # get tt ids from Timetable -table
        tt_str=$(export PGPASSWORD='111'; psql -h '172.17.0.2' -U 'kirill' \
            -d 'university' \
            -c "select id from Timetable t where t.groupId='$g_code';")
        readarray -t y <<< "$tt_str"
        unset y[0]
        unset y[1]
        unset y[-1]
        tt_ids=("${y[@]}"); #array
        # for each lesson set up visit for given student
        for (( j=0; j < ${#tt_ids[@]}; j++ ));
        do
            tt_id=${tt_ids[$j]};
            isVisited=$(get_isVisited $(($RANDOM % 2)));
            export PGPASSWORD='111'; psql -h '172.17.0.2' -U 'kirill' \
                -d 'university' \
                -c "INSERT INTO VISIT(studentId, isVisited, tt_id) 
                    VALUES ('$st_code', '$isVisited', $tt_id);"
        done
    done
}

build_visit