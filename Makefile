
# just type make run and relax...
run:
	docker-compose up -d
	sleep 120
	(cd ./MongoSinkScript && make run_b)

# it's necessary to use only this command
stop:
	docker stop mongo-sink-service && docker-compose down
