#!/usr/bin/zsh

if ! [[ -f /usr/bin/python3 ]]; then
  PYTHON=/usr/bin/python
else
  PYTHON=/usr/bin/python3
fi

$PYTHON ./distribute.py
$PYTHON ./install.py
