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
        cmd="docker network rm $name"
        $cmd > result.log
        
        if [ "$?" -eq 0 ]; then
            echo "ok - docker network delete passed"
        else
            echo "not ok - docker network delete failed"
        fi
    done

