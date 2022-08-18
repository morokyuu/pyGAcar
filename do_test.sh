ls -1 test_*.py | xargs -n1 python 2>&1 > /dev/null | grep -i fail
