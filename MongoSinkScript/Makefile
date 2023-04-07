
build:
	#docker image rm mongo_sink_service;
	docker build --network=host -t mongo_sink_service .;

run_b:
	make build;
	docker run --rm --name mongo-sink-service -d --network \
		softarchitecture_shared_net mongo_sink_service
run:
	docker run --rm --name mongo-sink-service -d --network \
		softarchitecture_shared_net mongo_sink_service
