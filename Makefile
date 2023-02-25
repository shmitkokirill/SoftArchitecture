
start_postgres:
	docker run \
	--rm \
	-it \
	--name postgres \
	-e POSTGRES_DB=test \
	-e POSTGRES_USER=kirill \
	-e POSTGRES_PASSWORD=111 \
	-p 5000:5432 \
	debezium/postgres

start_zookeeper:
	docker run \
	--rm \
	-it \
	--name zookeeper \
	-p 2181:2181 \
	-p 2888:2888 \
	-p 3888:3888 \
	debezium/zookeeper

start_kafka:
	docker run \
	--rm \
	-it \
	--name kafka \
	-p 9092:9092 \
	--link zookeeper:zookeeper \
	debezium/kafka

start_connector:
	docker run \
	-it \
	--name connect \
	-p 8083:8083 \
	-e GROUP_ID=1 \
	-e CONFIG_STORAGE_TOPIC=my-connect-configs \
	-e OFFSET_STORAGE_TOPIC=my-connect-offsets \
	-e ADVERTISED_HOST_NAME=$(echo $DOCKER_HOST | cut -f3 -d’/’ | cut -f1 -d’:’) \
	--link zookeeper:zookeeper \
	--link postgres:postgres \
	--link kafka:kafka \
	debezium/connect
