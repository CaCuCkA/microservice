#!/bin/bash

BASE_URL="http://localhost:5004"

post_message() {
    message=$1
    curl -s -X POST "$BASE_URL/msg" -H "Content-Type: application/json" -d "{\"msg\": \"$message\"}"
}

get_messages() {
    curl -s "$BASE_URL/msgs"
}

echo "Posting messages..."
for i in {1..10}; do
    response=$(post_message "Message $i")
    echo "Posted Message $i: $response"
    sleep 1 # Adds a 1-second delay between each POST request
done

echo ""
echo "Getting messages..."
messages=$(get_messages)

if command -v jq &> /dev/null; then
    echo $messages | jq
else
    echo "jq not found. Raw response:"
    echo $messages
fi
