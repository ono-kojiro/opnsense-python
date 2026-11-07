#!/bin/sh

echo "1..1"

docker compose down
if [ "$?" -eq 0 ]; then
    echo "ok - passed: docker compose down"
else
    echo "not ok - failed: docker compose down"
fi


