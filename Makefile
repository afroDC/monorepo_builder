define HELP
Commands:
  help             print this help text
  build-<PROJECT>  build the project
  deploy-<PROJECT> deploy the project
  test-<PROJECT>   test the project
  upload-<PROJECT> upload the project to it's repository. This should not be done manually
endef
export HELP

.PHONY: help
help:
	@echo "$${HELP}"

build-example-a: 
	@echo "Commands to build example a project."
build-example-b: 
	@echo "Commands to build example b project."

test-example-a: 
	@echo "Commands to test example a project after it's been built."
test-example-b: 
	@echo "Commands to test example b project after it's been built."

upload-example-a:
	@echo "Commands to upload example a after merges to master."
upload-example-b:
	@echo "Commands to upload example b after merges to master."

deploy-example-a:
	@echo "Commands to deploy example b after merges to master."
deploy-example-b:
	@echo "Commands to deploy example b after merges to master."

