#!/bin/bash

cd $(dirname $0)
source .venv/bin/activate

case $1 in
    clean)
        exec ./manage.py delete_expired_joints
    ;;
    *)
        exec gunicorn -b unix:/tmp/peqes.sock main.wsgi:application
    ;;
esac
