#!/bin/bash
virtualenv --no-site-packages ve && \
source ve/bin/activate && \
    pip install -r requirements.pip && \
    find ./ -name '*.pyc' -delete && \
    cd ummeli/ && \
    ./manage.py test --with-coverage --cover-erase --cover-package=ummeli --cover-html --with-xunit && \
    cd .. && \
    coverage xml --omit="ve/*" && \
    (pyflakes ummeli/ > pyflakes.log || true) && \
    (pep8 ummeli/ > pep8.log || true ) && \
deactivate
