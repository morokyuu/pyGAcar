#!/bin/bash
#  ref = https://itneko.com/shell-redirect-pipe/

ls -1 test_*.py | xargs -n1 python 2>&1 > /dev/null | grep -i fail
