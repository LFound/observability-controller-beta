#!/usr/bin/env bash

curl -X POST "$OBSERVABILITY_API_URL" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $OBSERVABILITY_API_KEY" \
  -d '{"message":"My deployment failed."}'
