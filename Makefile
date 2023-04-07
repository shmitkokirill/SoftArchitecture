
# just type make run and relax...
run:
	docker-compose up -d
	sleep 120
	(cd ./MongoSinkScript && make run_b)

autofill_pg:
	pip install psycopg2 && \
		(cd ./Scripts/Postgres && python postgre_autofill.py)

# it's necessary to use only this command
stop:
	docker stop mongo-sink-service && docker-compose down
