#
# This script does the following:
# - Sets PYTHONPATH
# - Sets an alias "t" for running unit tests
# - Sets an alias "tree" for hiding .pyc and __pycache__ from the tree command
#

export PYTHONPATH=.

alias t="py.test -q"
alias tree="tree -I \"*.pyc|__pycache__\""
