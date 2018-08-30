PWD ?= $(shell pwd)

tests:
	@pytest -s -vv
.PHONY: tests

build:
	@docker build -t danielfrg/httpmonitor:1.0 .

devtest:
	@docker run -v $(PWD)/scratch/log.txt:/var/log/access.log -v $(PWD)/scratch/log2.txt:/var/log/access2.log -it danielfrg/httpmonitor:1.0 -f /var/log/access.log -f /var/log/access2.log -i 3 -a 3 -t 10

run:
	@docker run -v $(PWD)/scratch/log.txt:/var/log/access.log -it danielfrg/httpmonitor:1.0

