#!/bin/sh

. ./common.shrc

num=$(cat categories.yml | yq -c '.categories | length')
# alias x2 + 2
num_test=$(expr $num \* 2)

echo "1..${num_test}"

cat categories.yml | yq -c '.categories[]' |
    while read -r item; do
        name=$(echo "$item" | jq -r '.name')
        color=$(echo "$item" | jq -r '.color')
        rm -f result.json
        $opncli firewall category add name=$name color=$color > result.json
        if [ "$?" -eq 0 ]; then
            echo "ok - opncli command passed"
        else
            echo "not ok - opncli command failed"
        fi

        result=$(cat result.json | jq -r ".result")
        if [ "$result" = "saved" ]; then
            echo "ok - result: $result"
        else
            reason=$(cat result.json | jq -r ".validations[]")
            echo "not ok - result: $result, reason: $reason"
        fi
done

