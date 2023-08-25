#!/bin/bash
cd $(dirname $0)
docker build -f docker/Dockerfile -t userien .
