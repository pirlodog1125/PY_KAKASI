#!/bin/sh
docker run --rm \
    -v /"$PWD"://var/task \
    lambci/lambda:build-python3.8 \
    bash -c "\
    pip freeze --path site-packages | tee requirements.txt && \
    echo 'pip freeze completed!!'
    "
