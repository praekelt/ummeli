from setuptools import setup, find_packages

def listify(filename):
    return filter(None, open(filename,'r').readlines())

setup(
    name = "ummeli",
    version = "1.9",
    url = 'http://github.com/praekelt/ummeli',
    license = 'BSD',
    description = "",
    long_description = open('README.rst','r').read(),
    author = 'Praekelt Foundation',
    author_email = 'dev@praekeltfoundation.org',
    packages = find_packages(),
    install_requires = ['setuptools'] + listify('requirements.pip'),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Private Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

