#!/usr/bin/env bats

load helper

@test "ignore builtin 1" {
  run ./bin/osh -n --ast-format command-names -c "echo foo"
  test_ok_empty || stdfail
}

@test "simple command 1" {
  run ./bin/osh -n --ast-format command-names -c "foo"
  test_ok_nonempty "foo" || stdfail
}

@test "pathname command 1" {
  run ./bin/osh -n --ast-format command-names -c "/bin/foo"
  test_ok_nonempty "/bin/foo" || stdfail 1
  run ./bin/osh -n --ast-format command-names -c "./foo"
  test_ok_nonempty "./foo" || stdfail 2
  run ./bin/osh -n --ast-format command-names -c "~/foo"
  test_ok_nonempty "~/foo" || stdfail 3
}

@test "pipeline command 1" {
  run ./bin/osh -n --ast-format command-names -c "echo bar | foo"
  test_ok_nonempty "foo" || stdfail
}

@test "subshell command 1" {
  run ./bin/osh -n --ast-format command-names -c "echo \$(printf \$(foo))"
  test_ok_nonempty "foo"
}

@test "vars 1 - default ignore" {
  run ./bin/osh -n --ast-format command-names -c "\$foo"
  test_ok_empty
}

@test "vars 2 - notations and prefixes" {
  run ./bin/osh -n --ast-format command-names --exec-vars '.*' -c "\$foo"
  test_ok_nonempty "$foo" || stdfail 1
  run ./bin/osh -n --ast-format command-names --exec-vars '.*' -c "\${foo}"
  test_ok_nonempty "$foo" || stdfail 2
  run ./bin/osh -n --ast-format command-names --exec-vars '.*' -c "sudo \$foo"
  test_ok_nonempty "$foo" || stdfail 3
  run ./bin/osh -n --ast-format command-names --exec-vars '.*' -c "sudo \${foo}"
  test_ok_nonempty "$foo" || stdfail 4

  run ./bin/osh -n --ast-format command-names --exec-vars '.*bar.*' -c "sudo \${foo}"
  test_ok_empty || stdfail 5
}

@test "prefixes 1 - default ignore" {
  run ./bin/osh -n --ast-format command-names -c "eval foo" ; test_ok_nonempty "foo"
  run ./bin/osh -n --ast-format command-names -c "sudo foo" ; test_ok_nonempty "foo"
  run ./bin/osh -n --ast-format command-names -c "time foo" ; test_ok_nonempty "foo"
  run ./bin/osh -n --ast-format command-names -c "sudo eval time foo" ; test_ok_nonempty "foo"
}

@test "prefixes 2 - override" {
  run ./bin/osh -n --ast-format command-names --exec-prefixes 'foo,bar' -c "foo bar baz arg"
  test_ok_nonempty "baz"
}
