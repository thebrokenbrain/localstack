include .env

## help: Print commands help.
.PHONY: help
help : Makefile
	@sed -n 's/^##//p' $<

## install: Start LocalStack
.PHONY: start
start:
	@echo "Starting LocalStack"
	docker compose up -d

## stop: Stop LocalStack
.PHONY: stop
stop:
	@echo "Stopping LocalStack"
	docker compose down

## configure: configure credentials for LocalStack
.PHONY: configure
configure:
	@echo "Configuring AWS"
	aws configure --profile localstack

## check-connection: check connection to LocalStack
.PHONY: check-connection
check-connection:
	@echo "Checking connection to LocalStack"
	aws --profile=localstack --endpoint-url=${LOCALSTACK_ENDPOINT_URL} sts get-caller-identity

## load-aliases: Load aliases
.PHONY: load-aliases
load-aliases:
	@echo "To load the aliases, run 'source aliases' in your current shell" 

## demo: Run python script demo
.PHONY: demo
demo:
	@echo "Running demo" 
	python3 main.py

%:
	@: