#!/bin/bash

if [ $# -eq 0 ]; then
  ~/appengine-python-sdk/dev_appserver.py .
else
  ~/appengine-python-sdk/dev_appserver.py --clear_datastore .
fi
