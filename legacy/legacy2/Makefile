run-db:
	docker build -t wandergrove-db ./services/database/
	source .env && docker run -d \
		-p 5432:5432 \
		-e POSTGRES_USER=$POSTGRES_USER \
		-e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
		-e POSTGRES_DB=$POSTGRES_DB \
		wandergrove-db

