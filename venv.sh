#!/bin/sh
set -eu

# POSIX compatible way to get the script directory
DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
DIR_NAME=$(basename "$DIR")

# defaults virtual environment name to the project folder name, when the VENV variable is not set
[ -z "${VENV-}" ] && VENV="$DIR_NAME"


# defaults virtual environment name to the project folder name, when the VENV variable is not set# defaults virtual environment name to the project folder name, when the VENV variable is not set
[ -z "${VENV_REQUIREMENTS-}" ] && VENV_REQUIREMENTS="$DIR/requirements.txt"

venv_run() {
    venv_setup
    pew in "$VENV" "$@"
  }

venv_enter() {
  venv_workon
}

venv_workon() {
  pew workon $VENV
}


venv_setup() {
      venv_exists "$VENV" || venv_create "$VENV"
  }

venv_update() {
      venv_fix
      venv_freeze
  }

venv_fix() {
      venv_delete
      venv_setup
  }

venv_delete() {
      pew rm "$VENV"
  }

venv_freeze() {
      venv_exists "$VENV" || error "the venv was never created. you may want to run ./run.sh venv_setup first"
      cd "$DIR"
      pew in "$VENV" pip freeze > $VENV_REQUIREMENTS
  }

venv_exists() {
      venv=$1
      pew ls | grep "$venv" > /dev/null
  }

venv_create() {
      venv=$1
      cd "$DIR"
      pew new "$venv" -d
      pew in "$venv" pip install -r $VENV_REQUIREMENTS
  }

error() {
      msg=$1
      echo "ERROR: $msg"
      exit 1
  }

is_installed() {
      cmd=$1
      command -v "$cmd" > /dev/null 2>&1
  }


is_installed pew || error "please, install pew (https://github.com/pew-org/pew)"
