#!/bin/bash

# les_ids_string=$(export PGPASSWORD='111'; psql -h localhost -p 5432 \
#             -U 'kirill' \
#             -d 'university' \
#             -c "select lessonid from Timetable;")
# readarray -t y <<< "$les_ids_string"
# unset y[0]
# unset y[1]
# unset y[-1]
# les_ids=("${y[@]}"); #array

# dates_string=$(export PGPASSWORD='111'; psql -h localhost -p 5432 \
#             -U 'kirill' \
#             -d 'university' \
#             -c "select date from Timetable;")
# readarray -t y <<< "$dates_string"
# unset y[0]
# unset y[1]
# unset y[-1]
# dates=("${y[@]}"); #array

# echo $(date -d "${dates[0]}" +%Y-%m-%d);

# for (( i=0; i<${#dates[@]}; i++ ));
# do 
#     d=$(date -d "${dates[$i]}" +%Y-%m-%d)
#     les_id="$(echo -e "${les_ids[$i]}" | tr -d '[:space:]')"  # trim
#     curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#         -H "Accept: application/json" -H 'Content-type: application/json' \
#         -d '{"statements": [{"statement": "CREATE (l:Lesson{date:\"'"$d"'\", id:\"'"$les_id"'\"});"}]}' \
#         -o log.out
# done





# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d "{\"statements\": \
#             [{\"statement\": \
#                 \"MATCH (a:Lesson), (b:Course) \
#                     WHERE a.id = '7' and b.title = 'Безопасность ПО' \
#                     CREATE (a)-[r:on_course]->(b) RETURN type(r);\"}]}" \
#     -o log.out
# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d "{\"statements\": \
#             [{\"statement\": \
#                 \"MATCH (a:Lesson), (b:Course) \
#                     WHERE a.id = '6' and b.title = 'Алгоритмы' \
#                     CREATE (a)-[r:on_course]->(b) RETURN type(r);\"}]}" \
#     -o log.out
# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d "{\"statements\": \
#             [{\"statement\": \
#                 \"MATCH (a:Lesson), (b:Course) \
#                     WHERE a.id = '8' and b.title = 'Алгоритмы' \
#                     CREATE (a)-[r:on_course]->(b) RETURN type(r);\"}]}" \
#     -o log.out
# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d "{\"statements\": \
#             [{\"statement\": \
#                 \"MATCH (a:Lesson), (b:Course) \
#                     WHERE a.id = '9' and b.title = 'Высшая математика' \
#                     CREATE (a)-[r:on_course]->(b) RETURN type(r);\"}]}" \
#     -o log.out
# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d "{\"statements\": \
#             [{\"statement\": \
#                 \"MATCH (a:Lesson), (b:Course) \
#                     WHERE a.id = '10' and b.title = 'Облака' \
#                     CREATE (a)-[r:on_course]->(b) RETURN type(r);\"}]}" \
#     -o log.out
# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d "{\"statements\": \
#             [{\"statement\": \
#                 \"MATCH (a:Lesson), (b:Course) \
#                     WHERE a.id = '11' and b.title = 'Безопасность ПО' \
#                     CREATE (a)-[r:on_course]->(b) RETURN type(r);\"}]}" \
#     -o log.out
# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d "{\"statements\": \
#             [{\"statement\": \
#                 \"MATCH (a:Lesson), (b:Course) \
#                     WHERE a.id = '12' and b.title = 'Архитектура' \
#                     CREATE (a)-[r:on_course]->(b) RETURN type(r);\"}]}" \
#     -o log.out
# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d "{\"statements\": \
#             [{\"statement\": \
#                 \"MATCH (a:Lesson), (b:Course) \
#                     WHERE a.id = '13' and b.title = 'Безопасность ПО' \
#                     CREATE (a)-[r:on_course]->(b) RETURN type(r);\"}]}" \
#     -o log.out
# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d "{\"statements\": \
#             [{\"statement\": \
#                 \"MATCH (a:Lesson), (b:Course) \
#                     WHERE a.id = '14' and b.title = 'Безопасность ПО' \
#                     CREATE (a)-[r:on_course]->(b) RETURN type(r);\"}]}" \
#     -o log.out
# curl -X POST "http://neo4j:111@localhost:7474/db/neo4j/tx/commit" \
#     -H "Accept: application/json" -H 'Content-type: application/json' \
#     -d "{\"statements\": \
#             [{\"statement\": \
#                 \"MATCH (a:Lesson), (b:Course) \
#                     WHERE a.id = '15' and b.title = 'Управление' \
#                     CREATE (a)-[r:on_course]->(b) RETURN type(r);\"}]}" \
#     -o log.out