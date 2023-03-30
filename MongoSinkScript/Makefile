
build:
	#docker image rm mongo_sink_service;
	docker build --network=host -t mongo_sink_service .;

run:
	make build;
	docker run --rm --name mongo-sink-service -it --network \
		softarchitecture_shared_net mongo_sink_service
