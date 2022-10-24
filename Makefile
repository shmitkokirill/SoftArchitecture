NETWORK := bridge
MOUNT_POINT := /home/kirill/programs/SoftArchitecture
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
	redis-server --save 60 1 --loglevel	verbose 

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
	docker run \
	--rm \
	--name elasticsearch \
	--network ${NETWORK} \
	-p 9200:9200 \
	-e "discovery.type=single-node" \
	-v ${MOUNT_POINT}/elastic:/usr/share/elasticsearch/config \
	-d \
	elasticsearch

stop_mongo:
	docker stop mongo

stop_redis:
	docker stop redis

stop_all:
	docker stop postgresql;
	stop_redis