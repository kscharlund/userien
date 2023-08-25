#!/bin/bash
tmpdir=${1:-/tmp}
docker rm -f userien
docker run -i -t -p 8080:80 -v ${tmpdir}:/opt/userien/tmp --name=userien userien
