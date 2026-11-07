#!/bin/sh

num=$(cat filters.yml | yq -c '.filters | length')
num_test=$(expr $num \* 2 + 2)

echo "1..${num_test}"

cat filters.yml | yq -c '.filters[]' |
    while read -r item; do
        descr=$(echo "$item" | jq -r '.description')
        categories=$(echo "$item" | jq -r '.categories')
        action=$(echo "$item" | jq -r '.action')
        interface=$(echo "$item" | jq -r '.interface')
        direction=$(echo "$item" | jq -r '.direction')
        ipprotocol=$(echo "$item" | jq -r '.ipprotocol')
        protocol=$(echo "$item" | jq -r '.protocol')
        source_net=$(echo "$item" | jq -r '.source_net')
        destination_net=$(echo "$item" | jq -r '.destination_net')
        destination_port=$(echo "$item" | \
            jq -r '.destination_port // empty')
        enabled=$(echo "$item" | jq -r '.enabled')
        quick=$(echo "$item" | jq -r '.quick')
        statetype=$(echo "$item" | jq -r '.statetype')
        sequence=$(echo "$item" | jq -r '.sequence')

        #cmd="opncli -d firewall filter add_rule"
        cmd="opncli firewall filter add_rule"

        cmd="$cmd description=\"$descr\""
        cmd="$cmd categories=\"$categories\""
        cmd="$cmd action=\"$action\""
        cmd="$cmd interface=\"$interface\""
        cmd="$cmd direction=\"$direction\""
        cmd="$cmd ipprotocol=\"$ipprotocol\""
        cmd="$cmd protocol=\"$protocol\""
        cmd="$cmd source_net=\"$source_net\""
        cmd="$cmd destination_net=\"$destination_net\""
        if [ ! -z "$destination_port" ]; then
          cmd="$cmd destination_port=\"$destination_port\""
        fi
        cmd="$cmd quick=\"$quick\""
        cmd="$cmd statetype=\"$statetype\""
        cmd="$cmd sequence=\"$sequence\""
        echo $cmd 1>&2
        eval "$cmd" > result.json

        if [ "$?" -eq 0 ]; then
            echo "ok - opncli passed"
        else
            echo "not ok - opncli failed"
            echo "<<<<<<<<<<<<<<<"
            cat result.json
            echo ">>>>>>>>>>>>>>>"
        fi

        res=`cat result.json | jq -r ".result"`
        if [ "$res" = "saved" ]; then
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

