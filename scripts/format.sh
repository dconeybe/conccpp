#!/bin/bash

set -euo pipefail

function print_help {
cat << EOF
Syntax: $0 [options]

Options:
  -h Print this help message.
  -c Only check the files for formatting errors, but do not modify them;
       returns an exit code of 0 if no changes would be made, non-zero otherwise.
EOF
}

function parse_args {
  local arg_check_only=0

  while getopts ":ch" arg; do
    case $arg in
      h)
        print_help
        exit 0
        ;;
      c)
        arg_check_only=1
        ;;
      *)
        echo "ERROR: invalid flag: $OPTARG" >&2
        echo "Run with -h for help" >&2
        exit 2
        ;;
    esac
  done

  readonly ARG_CHECK_ONLY=$arg_check_only

  if [[ $OPTIND -le $# ]] ; then
    echo "ERROR: unexpected argument: $1" >&2
    echo "Run with -h for help" >&2
    exit 2
  fi
}

function run_pyink {
  local pyink_args=(
    pyink
    --line-length 100
    --target-version py311
    --pyink
    --pyink-indentation 2
    cmake/test/*.py
    workflows/checks/*.py
  )

  if [[ $ARG_CHECK_ONLY == '1' ]] ; then
    pyink_args+=(
      --check
      --diff
    )
  fi

  echo "${pyink_args[*]}"
  exec "${pyink_args[@]}"
}

parse_args "$@"
run_pyink
