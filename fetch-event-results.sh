#!/bin/bash
curl -H "ApiKey: $(cat eventor-api-key.txt)" "https://eventor.orientering.se/api/results/event/iofxml?eventId=$1"
