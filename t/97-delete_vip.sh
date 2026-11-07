#!/bin/sh

num=$(cat vips.yml | yq -c '.vips | length')
num_test=$(expr $num \* 2 + 2)

# x2 + 2
echo "1..${num_test}"

cat vips.yml | yq -c '.vips[]' |
    while read -r item; do
        iface=$(echo "$item" | jq -r '.interface')
        nw=$(echo "$item" | jq -r '.network')
        descr=$(echo "$item" | jq -r '.descr')
        opncli interfaces vip_settings del_item --descr="$descr" > result.json
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
opncli interfaces vip_settings reconfigure > result.json
if [ "$?" -eq 0 ]; then
    echo "ok - opncli passed"
else
    echo "not ok - opncli failed"
    echo "<<<<<<<<<<<<<<<"
    cat result.json
    echo ">>>>>>>>>>>>>>>"
fi

res=`cat result.json | jq -r ".status"`
if [ "$res" = "ok" ]; then
    echo "ok - reconfigure passed"
else
    echo "not ok - reconfigure failed"
    echo "<<<<<<<<<<<<<<<"
    cat result.json
    echo ">>>>>>>>>>>>>>>"
fi

