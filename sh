#!/bin/sh
set -e

verbosity=7
scriptpath=$HOME/bin . $HOME/bin/util.sh

lib_load vc build

#component_map=component_map_basenameid

component_map=component_map_list
component_tests=component_map_tests

build_init
#component_map_list test/osh-command-names-visitor-spec.bats
#component_map_list test/osh-var-names-visitor-spec.bats

#project_tests "$@"
#exit $?

exec_watch_scm
exit $?

exec_watch_scm_paths()
{
  vc_modified
  echo .git/index
}
exec_watch_poll_pathlist exec_watch_scm_paths test_scm
exit $?


# TODO: look at local (test) shellscripts or some other corpus too
for x in ~/bin/*.lib.sh ~/bin/commands/*.sh ~/bin/contexts/*.sh
do

  ./bin/osh -n --ast-format command-names "$x" ||
    echo "In $x" >&2

done >/dev/null
