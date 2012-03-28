#!/bin/bash
if not 've/';
then
    virtualenv --no-site-packages ve
fi
source ve/bin/activate && \
    pip install -r requirements.pip && \
    find ./ -name '*.pyc' -delete && \
    cd ummeli/ && \
    ./manage.py test --settings=test_settings --with-coverage --cover-erase --cover-package=ummeli --cover-html --with-xunit && \
    coverage xml --omit="../ve/*" && \
    cd .. && \
    (pyflakes ummeli/ > pyflakes.log || true) && \
    (pep8 ummeli/ > pep8.log || true ) && \
deactivate
