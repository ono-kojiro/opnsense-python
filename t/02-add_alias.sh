#!/bin/sh


num=$(cat aliases.yml | yq -c '.aliases | length')
num_test=$(expr $num \* 2 + 2)

# num alias x2 + 2
echo "1..${num_test}"

cat aliases.yml | yq -c '.aliases[]' |
    while read -r item; do
        name=$(echo "$item" | jq -r '.name')
        tname=$(echo "$item" | jq -r '.type')
        content=$(echo "$item" | jq -r '.content')
        enabled=$(echo "$item" | jq -r '.enabled')
        description=$(echo "$item" | jq -r '.description')
        opncli firewall alias add_item \
            name="$name" \
            type="$tname" \
            content="$content" \
            enabled="$enabled" \
            description="$description" > result.json
        if [ "$?" -eq 0 ]; then
            echo "ok - opncli passed"
        else
            echo "not ok - opncli failed"
        fi

        res=`cat result.json | jq -r ".result"`
        if [ "$res" = "saved" ]; then
            echo "ok - $res"
        else
            echo "not ok - $res"
        fi
    done


rm -f result.json
opncli firewall alias reconfigure > result.json
if [ "$?" -eq 0 ]; then
    echo "ok - opncli passed"
else
    echo "not ok - opncli failed"
fi

res=`cat result.json | jq -r ".status"`
if [ "$res" = "ok" ]; then
    echo "ok - reconfigure passed"
else
    echo "not ok - reconfigure failed"
fi

