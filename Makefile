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

start_redis:
	docker run \
	--rm \
	--name redis \
	--network ${NETWORK} \
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

start_elastic:
	# 1. sudo sysctl -w vm.max_map_count=262144    - malloc reference
	# 2. command below:
	docker run \
	--rm \
	--name elasticsearch \
	--net ${NETWORK} \
	-p 9200:9200 \
	-p 9300:9300 \
	-e ELASTIC_PASSWORD=111111 \
	-d \
	docker.elastic.co/elasticsearch/elasticsearch:8.4.3

	# docker cp \
	# elasticsearch:/usr/share/elasticsearch/config/certs/http_ca.crt \
	# ${MOUNT_POINT}/elastic/

	# When container is running:
	# docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password
	# docker cp elasticsearch:/usr/share/elasticsearch/config/certs/http_ca.crt .
	# check : curl --cacert elastic/http_ca.crt -u elastic https://localhost:9200
	# -v ${MOUNT_POINT}/elastic/data:/usr/share/elasticsearch/data \
	# -v elasticVol:/usr/share/elasticsearch/config/certs \

start_neo:
	docker run \
	--rm \
	--name neo4j \
	--network ${NETWORK} \
    -p 7474:7474 \
	-p 7687:7687 \
    -v ${MOUNT_POINT}/neo4j/data:/data \
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
