#!/bin/sh

echo "Waiting for Consul to become ready..."
while ! curl -s http://localhost:8500/v1/status/leader | grep -qE '".+"'; do
  sleep 1
done
  
echo "Consul is ready."

echo "Adding KV pairs..."
curl -X PUT -d 'comm-queue' http://localhost:8500/v1/kv/queue_name
curl -X PUT -d 'messages-map' http://localhost:8500/v1/kv/map_name

echo "KV pairs added."
