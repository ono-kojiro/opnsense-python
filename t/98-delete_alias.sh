#!/bin/sh

num=$(cat aliases.yml | yq -c '.aliases | length')
num_test=$(expr $num \* 2 + 1)

# num alias x2 + 2
echo "1..${num_test}"

cat aliases.yml | yq -c '.aliases[]' |
    while read -r item; do
        name=$(echo "$item" | jq -r '.name')
        rm -f result.json
        #echo "DEBUG: name is $name"
        opncli firewall alias delete --name=\"$name\" > result.json
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
opncli firewall alias reconfigure > result.json
if [ "$?" -eq 0 ]; then
    echo "ok - alias reconfigure passed"
else
    echo "not ok - alias reconfigure failed"
fi

