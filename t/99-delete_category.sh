#!/bin/sh

. ./common.shrc

num=$(cat categories.yml | yq -c '.categories | length')

# num categories x 2
num_test=$(expr $num \* 2)

echo "1..${num_test}"

cat categories.yml | yq -c '.categories[]' |
    while read -r item; do
        name=$(echo "$item" | jq -r '.name')

        rm -f result.json
        $opncli firewall category del_item --name=$name > result.json
        if [ "$?" -eq 0 ]; then
            echo "ok - opncli passed"
        else
            echo "ok - opncli failed"
        fi

        result=$(cat result.json | jq -r ".result")
        if [ "$result" = "deleted" ]; then
            echo "ok - $result"
        else
            reason=$(cat result.json | jq -r ".validations[]")
            echo "not ok - result: $result, reason: $reason"
        fi
    done


