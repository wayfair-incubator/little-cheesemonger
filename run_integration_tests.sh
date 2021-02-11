#!/usr/bin/env bash
set -e

docker-compose run --rm test-integration-manylinux1-default-loader
docker-compose run --rm test-integration-manylinux1-custom-loader
docker-compose run --rm test-integration-manylinux2010-default-loader
docker-compose run --rm test-integration-manylinux2010-custom-loader
docker-compose run --rm test-integration-manylinux2014-default-loader
docker-compose run --rm test-integration-manylinux2014-custom-loader
