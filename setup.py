# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215)
import multiprocessing
assert multiprocessing
import re
from setuptools import setup, find_packages


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'switchenv/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


install_requires = [
    'click',
    'fuzzypicker'
]

tests_require = [
    'coverage',
    'flake8',
    'mock',
    'nose',
    'wheel',
]

docs_require = [
    'Sphinx',
    'sphinx_rtd_theme'
]

extras_require = {
    'dev': tests_require + docs_require,
}

setup(
    name='switchenv',
    version=get_version(),
    description='Manager for bash environments',
    description_content_type='text/markdown',
    long_description='Manger for bash environments',
    long_description_content_type='text/markdown',
    url='https://github.com/robdmc/switchenv',
    author='Rob deCarvalho',
    author_email='unlisted@unlisted.net',
    keywords='',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    include_package_data=True,
    test_suite='nose.collector',
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'switchenv = switchenv.switchenv:main',
            'sw = switchenv.switchenv:main',
        ],
    }
)
