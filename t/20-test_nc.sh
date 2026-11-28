#!/bin/sh

. ./common.shrc

num=$(cat testcase.yml | yq -c '.testcases | length')
num_test=$(expr $num \* 3)

echo "1..${num_test}"

cat testcase.yml | yq -c '.testcases[]' |
    while read -r item; do
        dstterm=$(echo "$item" | jq -r '.dstterm')
        srcterm=$(echo "$item" | jq -r '.srcterm')
        dstcmd=$(echo "$item" | jq -r '.dstcmd')
        dstkillcmd=$(echo "$item" | jq -r '.dstkillcmd')
        srccmd=$(echo "$item" | jq -r '.srccmd')
       
	    echo "dstterm: $dstterm, srcterm: $srcterm"
		echo "dstcmd: $dstcmd"
		echo "srccmd: $srccmd"
		echo "dstkillcmd: $dstcmd"

		docker exec -d $dstterm $dstcmd
        if [ "$?" -eq 0 ]; then
            echo "ok - docker exec detach $dstterm"
        else
            echo "not ok - docker exec detach $dstterm"
        fi

		docker exec $srcterm $srccmd
        if [ "$?" -eq 0 ]; then
            echo "ok - docker exec $srcterm"
        else
            echo "not ok - docker exec $srcterm"
        fi

		docker exec $dstterm $dstkillcmd
        if [ "$?" -eq 0 ]; then
            echo "ok - docker exec $dstterm"
        else
            echo "not ok - docker exec $dstterm"
        fi
    done


