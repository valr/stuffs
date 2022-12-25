# use default or current directory for temporary directories/files
# set tempdir := "."

# list the recipes
default:
  @just --justfile {{justfile()}} --list --list-heading '' --unsorted

# initialise the virtual environment
init-venv:
  #!/usr/bin/env bash
  set -euo pipefail
  [ -d .venv ] && { echo "error: the virtual environment .venv already exists"; false; }
  python -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip setuptools wheel
  pip install --upgrade pip-tools

# install the requirements
install-requirements:
  #!/usr/bin/env bash
  set -euo pipefail
  [ ! -d .venv ] && { echo "error: the virtual environment .venv doesn't exist"; false; }
  source .venv/bin/activate
  pip-sync requirements.txt

# compile the requirements
compile-requirements:
  #!/usr/bin/env bash
  set -euo pipefail
  [ ! -d .venv ] && { echo "error: the virtual environment .venv doesn't exist"; false; }
  source .venv/bin/activate
  pip-compile --quiet requirements.in

# upgrade the requirements
upgrade-requirements:
  #!/usr/bin/env bash
  set -euo pipefail
  [ ! -d .venv ] && { echo "error: the virtual environment .venv doesn't exist"; false; }
  source .venv/bin/activate
  pip-compile --quiet --upgrade requirements.in
