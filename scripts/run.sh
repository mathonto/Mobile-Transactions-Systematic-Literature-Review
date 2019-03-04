#!/bin/bash

docker build -t search-script .
docker run -d -v "$(pwd)":/app search-script