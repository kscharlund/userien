#!/bin/bash
tmpdir=${1:-/tmp}
docker rm -f userien
docker run -d --restart unless-stopped -p 8080:8080 -v ${tmpdir}:/opt/userien/tmp --name=userien userien
