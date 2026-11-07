#!/bin/sh

num=$(cat networks.yml | yq -c '.networks | length')
num_test=$(expr $num)

echo "1..${num_test}"

cat networks.yml | yq -c '.networks[]' |
    while read -r item; do
        name=$(echo "$item" | jq -r '.name')
        parent=$(echo "$item" | jq -r '.parent')
        driver=$(echo "$item" | jq -r '.driver')
        gateway=$(echo "$item" | jq -r '.gateway')
        subnet=$(echo "$item" | jq -r '.subnet')
        cmd="docker network create -d $driver"
        cmd="$cmd --subnet=$subnet"
        cmd="$cmd --gateway=$gateway"
        cmd="$cmd --opt parent=$parent"
        cmd="$cmd $name"
        $cmd > result.log
        
        if [ "$?" -eq 0 ]; then
            echo "ok - docker network create passed"
        else
            echo "not ok - docker network create failed"
        fi
    done

