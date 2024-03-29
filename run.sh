#!/bin/sh
set -eu

# POSIX compatible way to get the script directory
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

VENV="cs2_lobby_share"
. "${DIR}/venv.sh"


run(){
  . $DIR/.env
  venv_run python main.py
}


"$@"
