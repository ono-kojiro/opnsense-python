#!/bin/sh

num=$(cat categories.yml | yq -c '.categories | length')
# alias x2 + 2
num_test=$(expr $num \* 2)

echo "1..${num_test}"

cat categories.yml | yq -c '.categories[]' |
    while read -r item; do
        name=$(echo "$item" | jq -r '.name')
        color=$(echo "$item" | jq -r '.color')
        rm -f result.json
        opncli firewall category add name=$name color=$color > result.json
        if [ "$?" -eq 0 ]; then
            echo "ok - opncli passed"
        else
            echo "not ok - opncli failed"
        fi

        res=`cat result.json | jq -r ".result"`
        if [ "$res" = "saved" ]; then
            echo "ok - $category: $res"
        else
            echo "not ok - $category: $res"
        fi
done

