#!/bin/sh
python $VIRTUAL_ENV/manage.py dumpdata --natural -e contenttypes -e admin -e sessions -e auth -e reversion --indent=4