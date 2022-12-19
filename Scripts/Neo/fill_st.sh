#!/bin/bash


# get stud cods from GroupStudent -table
st_cods_str=$(export PGPASSWORD='111'; psql -h '172.17.0.3' -U 'kirill' \
    -d 'university' -c "select code_st from GroupStudent where code_group = 'БИСО-01-19';")
readarray -t y <<< "$st_cods_str"
unset y[0]
unset y[1]
unset y[-1]
st_cods=("${y[@]}"); #array

# get group cods from GroupStudent -table
g_cods_str=$(export PGPASSWORD='111'; psql -h '172.17.0.3' -U 'kirill' \
    -d 'university' -c "select code_group from GroupStudent where code_group = 'БИСО-01-19';")
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
        -d '{"statements": [{"statement": "CREATE (p:Student{code:\"'"$st_code"'\", g_code:\"'"$g_code"'\"});"}]}' \
        -o log.out
done

# # get group cods from GroupStudent -table
# g_cods_str=$(export PGPASSWORD='111'; psql -h '172.17.0.2' -U 'kirill' \
#     -d 'university' -c 'select code from groups;')
# readarray -t y <<< "$g_cods_str"
# unset y[0]
# unset y[1]
# unset y[-1]
# g_cods=("${y[@]}"); #array

# # get group cods from GroupStudent -table
# g_specs_str=$(export PGPASSWORD='111'; psql -h '172.17.0.2' -U 'kirill' \
#     -d 'university' -c 'select spec from groups;')
# readarray -t y <<< "$g_specs_str"
# unset y[0]
# unset y[1]
# unset y[-1]
# g_specs=("${y[@]}"); #array

# for (( i=0; i<${#g_cods[@]}; i++ ));
# do 
#     g_code="$(echo -e "${g_cods[$i]}" | tr -d '[:space:]')"  # trim
#     g_spec="$(echo -e "${g_specs[$i]}" | tr -d '[:space:]')"  # trim
#     curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#         -H "Accept: application/json" -H 'Content-type: application/json' \
#         -d '{"statements": [{"statement": "CREATE (g:Group{code:\"'"$g_code"'\",spec:\"'"$g_spec"'\"});"}]}' \
#         -o log.out
# done

# #insert relations
# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d '{"statements": [{"statement": "MATCH (a:Student), (b:Group) WHERE a.g_code = b.code CREATE (a)-[r:member_of]->(b);"}]}' \
#     -o log.out

# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d '{"statements": [{"statement": "MATCH (a:Group), (b:Specialty) WHERE a.spec = b.code CREATE (a)-[r:member_of]->(b);"}]}' \
#     -o log.out
