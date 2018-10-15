#!/bin/sh
set -e

# TODO: look at local (tesT) shellscripts or some other corpus too
for x in ~/bin/*.lib.sh ~/bin/commands/*.sh ~/bin/contexts/*.sh
do

  ./bin/osh -n --ast-format command-names "$x" ||
    echo "In $x" >&2

done >/dev/null
