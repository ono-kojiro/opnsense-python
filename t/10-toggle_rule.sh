#!/bin/sh

. ./common.shrc

num=$(cat filters.yml | yq -c '.filters | length')
num_test=$(expr 3 + $num \* 6)

echo "1..$num_test"

cmd="$opncli firewall filter search_rule"
eval "$cmd" > search_rule_before.json
if [ "$?" -eq 0 ]; then
  echo "ok - search_rule passed"
else
  echo "not ok - search_rule failed"
fi

cat search_rule_before.json | jq -c '
  .rows[]
  | select(."%categories" == "red")
  | {
      uuid,
      enabled,
      categories,
      "%categories",
      description
    }
  ' | \
  while read -r item; do
      uuid=$(echo "$item" | jq -r '.uuid')
      enabled=$(echo "$item" | jq -r '.enabled')
      descr=$(echo "$item" | jq -r '.description')
      category=$(echo "$item" | jq -r '."%categories"')
      echo "DEBUG: $category, $uuid, $enabled, $descr"

      $opncli firewall filter set_rule enabled=0 --descr="$descr"
      if [ "$?" -eq 0 ]; then
          echo "ok - set_rule passed"
      else
          echo "not ok - set_rule failed"
      fi

      $opncli firewall filter apply
      if [ "$?" -eq 0 ]; then
          echo "ok - apply passed"
      else
          echo "not ok - apply failed"
      fi
  done

cmd="$opncli firewall filter search_rule"
eval "$cmd" > search_rule_after.json
if [ "$?" -eq 0 ]; then
  echo "ok - search_rule passed"
else
  echo "not ok - search_rule failed"
fi

cat search_rule_after.json | jq -c '
  .rows[]
  | select(."%categories" == "red")
  | {
      uuid,
      enabled,
      categories,
      "%categories",
      description
    }
  ' | \
  while read -r item; do
      uuid=$(echo "$item" | jq -r '.uuid')
      enabled=$(echo "$item" | jq -r '.enabled')
      descr=$(echo "$item" | jq -r '.description')
      category=$(echo "$item" | jq -r '."%categories"')
      echo "DEBUG: $category, $uuid, $enabled, $descr"
      if [ "$enabled" -eq 0 ]; then
          echo "ok - set_rule passed"
      else
          echo "not ok - set_rule failed"
      fi

  done


#
# enable again
#
cat search_rule_before.json | jq -c '
  .rows[]
  | select(."%categories" == "red")
  | {
      uuid,
      enabled,
      categories,
      "%categories",
      description
    }
  ' | \
  while read -r item; do
      uuid=$(echo "$item" | jq -r '.uuid')
      enabled=$(echo "$item" | jq -r '.enabled')
      descr=$(echo "$item" | jq -r '.description')
      category=$(echo "$item" | jq -r '."%categories"')

      $opncli firewall filter set_rule enabled=1 --descr="$descr"
      if [ "$?" -eq 0 ]; then
          echo "ok - set_rule passed"
      else
          echo "not ok - set_rule failed"
      fi

      $opncli firewall filter apply
      if [ "$?" -eq 0 ]; then
          echo "ok - apply passed"
      else
          echo "not ok - apply failed"
      fi
  done

#
# check again
#   
cmd="$opncli firewall filter search_rule"
eval "$cmd" > search_rule_end.json

if [ "$?" -eq 0 ]; then
  echo "ok - search_rule passed"
else
  echo "not ok - search_rule failed"
fi

cat search_rule_end.json | jq -c '
  .rows[]
  | select(."%categories" == "red")
  | {
      uuid,
      enabled,
      categories,
      "%categories",
      description
    }
  ' | \
  while read -r item; do
      uuid=$(echo "$item" | jq -r '.uuid')
      enabled=$(echo "$item" | jq -r '.enabled')
      descr=$(echo "$item" | jq -r '.description')
      category=$(echo "$item" | jq -r '."%categories"')
      echo "DEBUG: $category, $uuid, $enabled, $descr"
      if [ "$enabled" -eq 1 ]; then
          echo "ok - set_rule passed"
      else
          echo "not ok - set_rule failed"
      fi
  done

exit 0

