#!/bin/sh

num=$(cat filters.yml | yq -c '.filters | length')
num_test=$(expr $num \* 2 + 2)

echo "1..${num_test}"

cat filters.yml | yq -c '.filters[]' |
    while read -r item; do
        descr=$(echo "$item" | jq -r '.description')

        opncli firewall filter del_rule --descr="$descr" > result.json

        if [ "$?" -eq 0 ]; then
            echo "ok - opncli passed"
        else
            echo "not ok - opncli failed"
            echo "<<<<<<<<<<<<<<<"
            cat result.json
            echo ">>>>>>>>>>>>>>>"
        fi

        res=`cat result.json | jq -r ".result"`
        if [ "$res" = "deleted" ]; then
            echo "ok - $res"
        else
            echo "not ok - $res"
            echo "<<<<<<<<<<<<<<<"
            cat result.json
            echo ">>>>>>>>>>>>>>>"
        fi
    done

rm -f result.json
opncli firewall filter apply > result.json
if [ "$?" -eq 0 ]; then
    echo "ok - opncli passed"
else
    echo "not ok - opncli failed"
    echo "<<<<<<<<<<<<<<<"
    cat result.json
    echo ">>>>>>>>>>>>>>>"
fi

res=`cat result.json | jq -r ".status"`
if [ "$res" = "OK" ]; then
    echo "ok - apply passed"
else
    echo "not ok - apply failed"
    echo "<<<<<<<<<<<<<<<"
    cat result.json
    echo ">>>>>>>>>>>>>>>"
fi

