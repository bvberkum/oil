#!/usr/bin/env bats

load helper

@test "all vars" {
  run ./bin/osh -n --ast-format var-names -c 'echo $foo $bar'
  test_ok_nonempty '$foo $bar' || stdfail 1
  run ./bin/osh -n --ast-format var-names -c 'echo ${foo}'
  test_ok_nonempty '$foo' || stdfail 2
  run ./bin/osh -n --ast-format var-names -c 'echo $(( ${foo} + 1 ))'
  test_ok_nonempty '$foo' || stdfail 2
  run ./bin/osh -n --ast-format var-names -c 'echo foo bar'
  test_ok_empty || stdfail 3
}
