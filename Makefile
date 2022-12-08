NETWORK := bridge
MOUNT_POINT := $(shell pwd)
start_postgres:
	docker run \
	--rm \
	--network ${NETWORK} \
	--name postgresql \
	-e POSTGRES_DB=test \
	-e POSTGRES_USER=kirill \
	-e POSTGRES_PASSWORD=111 \
	-e PGDATA=/var/lib/postgresql/data/pgdata \
	-v ${MOUNT_POINT}/postgresql:/var/lib/postgresql/data \
	-p 5432:5432 \
	-d \
	postgres \
	-c log_statement=all

	# docker run -it --rm --network bridge postgres psql -h 172.17.0.2 -U kirill test

start_redis:
	docker run \
	--rm \
	--name redis \
	--network ${NETWORK} \
	-p 6379:6379 \
	-d \
	-v ${MOUNT_POINT}/redis:/data \
	redis \
	redis-server --save 60 1 --loglevel verbose 
	#docker run -it --network bridge --rm redis redis-cli -h 172.17.0.2

start_mongo:
	docker run \
	--rm \
	--network ${NETWORK} \
	--name mongo \
	-e MONGO_INITDB_ROOT_USERNAME=kirill \
	-e MONGO_INITDB_ROOT_PASSWORD=111 \
	-v ${MOUNT_POINT}/mongo:/data/db \
	-d \
	mongo
	# docker run -it --network ${NETWORK} --rm mongo mongosh --host 172.17.0.2 mongo
	# docker exec -it mongo bash
	## mongosh -u kirill -p 111 admin
	## use testDB
	#docker exec -it mongo mongosh -u kirill -p 111 admin

start_elastic:
	sudo sysctl -w vm.max_map_count=262144
	# 2. command below:
	docker run \
	--rm \
	--name elasticsearch \
	--net ${NETWORK} \
	-p 9200:9200 \
	-e ELASTIC_PASSWORD=111111 \
	-e "discovery.type=single-node" \
	-v ${MOUNT_POINT}/elastic:/usr/share/elasticsearch/data \
	-v ${MOUNT_POINT}/elastic:/usr/share/elasticsearch/config/certs \
	-d \
	docker.elastic.co/elasticsearch/elasticsearch:8.4.3

	# docker cp elasticsearch:/usr/share/elasticsearch/config/certs/http_ca.crt ./elastic/	

	# When container is running:
	# curl -u elastic -X GET "http://localhost:9200/lessons/_doc/1?pretty"
	## curl -X PUT "https://[localhost]:9200/indexname/_doc/1?pretty" -H 'Content-Type: application/json' -d '{ "field" : "value" }'
	## curl --cacert elastic/http_ca.crt -u elastic -X GET "https://localhost:9200/newindex/_doc/1?pretty"
	## curl --cacert elastic/http_ca.crt -u elastic -X DELETE "https://localhost:9200/newindex/_doc/1?pretty"

start_neo:
	# u: neo4j, p: 111
	docker run \
	--rm \
	--name neo4j \
	--network ${NETWORK} \
    -p 7474:7474 \
	-p 7687:7687 \
    -v ${MOUNT_POINT}/neo4j/data:/data \
	-v ${MOUNT_POINT}/neo4j/logs:/logs \
	-v ${MOUNT_POINT}/neo4j/conf:/conf \
	-d \
    neo4j

stop_neo:
	docker stop neo4j

stop_elastic:
	docker stop elasticsearch

stop_mongo:
	docker stop mongo

stop_redis:
	docker stop redis

stop_postgres:
	docker stop postgresql
