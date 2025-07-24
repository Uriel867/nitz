#!/bin/bash

# extracting the data
RESPONSE=$(curl -s $EXTRACT_URL)

# loading it to the db
curl -X POST \
  $LOAD_URL \
  -H 'Content-Type: application/json' \
  --data "$RESPONSE"
