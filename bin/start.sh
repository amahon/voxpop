#!/usr/bin/env bash

docker run -d -p 5672:5672 -p 15672:15672 -v ~/Projects/voxpop/log:/data/log -v ~/Projects/voxpop/data:/data/mnesia dockerfile/rabbitmq
docker run -d -p 6379:6379 -v ~/Projects/voxpop/data:/data --name redis dockerfile/redis redis-server /etc/redis/redis.conf --requirepass voxpop
docker run -d -p 27017:27017 -v ~/Projects/voxpop/data:/data/db --name mongodb dockerfile/mongodb