#!/bin/bash

URL=http://localhost:8000/predict
DURATION=30s
CONCURRENCY=10
QPS=50

hey -z $DURATION -c $CONCURRENCY -q $QPS \
  -m POST \
  -H "Content-Type: application/json" \
  -d '{"data":[1,2,3]}' \
  $URL
