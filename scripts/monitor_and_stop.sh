#!/bin/bash

stop_corresponding_hazelcast_node() {
  local service_name=$1
  case $service_name in
    logging_service_1)
      echo "Stopping hazelcast-node1..."
      docker stop hazelcast-node1
      ;;
    logging_service_2)
      echo "Stopping hazelcast-node2..."
      docker stop hazelcast-node2
      ;;
    logging_service_3)
      echo "Stopping hazelcast-node3..."
      docker stop hazelcast-node3
      ;;
    *)
      echo "No action needed for $service_name"
      ;;
  esac
}

docker events --filter 'event=stop' --format '{{.Actor.Attributes.name}}' | while read container_name; do
  echo "$container_name has stopped"
  stop_corresponding_hazelcast_node "$container_name"
done
