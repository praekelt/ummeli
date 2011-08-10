#!/bin/bash
virtualenv --no-site-packages ve && \
source ve/bin/activate && \
    pip install -r requirements.pip && \
    ./manage.py test --with-coverage --cover-erase --cover-package=core --cover-html --with-xunit && \
    coverage xml --omit="ve/*" && \
deactivate