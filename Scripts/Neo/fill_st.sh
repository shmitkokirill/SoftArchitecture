#!/bin/bash


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

for (( i=0; i<${#st_cods[@]}; i++ ));
do 
    st_code="$(echo -e "${st_cods[$i]}" | tr -d '[:space:]')"  # trim
    g_code="$(echo -e "${g_cods[$i]}" | tr -d '[:space:]')"  # trim
    curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
        -H "Accept: application/json" -H 'Content-type: application/json' \
        -d '{"statements": [{"statement": "CREATE (p:Person{code:\"'"$st_code"'\", g_code:\"'"$g_code"'\"});"}]}' \
        -o log.out
done

# insert one group
curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
    -H "Accept: application/json" -H 'Content-type: application/json' \
    -d '{"statements": [{"statement": "CREATE (g:Group{code:\"БСБО-01-19\"});"}]}' \
    -o log.out

#insert relations
curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
    -H "Accept: application/json" -H 'Content-type: application/json' \
    -d '{"statements": [{"statement": "MATCH (a:Person), (b:Group) WHERE a.g_code = b.code CREATE (a)-[r:member_of]->(b);"}]}' \
    -o log.out
