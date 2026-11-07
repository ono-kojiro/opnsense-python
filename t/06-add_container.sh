#!/bin/sh

echo "1..2"

docker compose up --no-start
if [ "$?" -eq 0 ]; then
    echo "ok - passed: docker compose up --no-start"
else
    echo "not ok - failed: docker compose up --no-start"
fi

docker compose start
if [ "$?" -eq 0 ]; then
    echo "ok - passed: docker compose start"
else
    echo "not ok - failed: docker compose start"
fi


