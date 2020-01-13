#!/usr/bin/env python

from os import path
from setuptools import find_packages, setup
this_directory = path.abspath(path.dirname(__file__))

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='mental models',
    version='0.1.1',
    description='Extracts human mental models from text and facilitates mental model comparison and contrasting. (See J Diesner 2003)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Kwame Porter Robinson",
    author_email='kwamepr@umich.edu',
    url='https://github.com/robinsonkwame/mental_models',
    packages=find_packages(include=['mental_models*']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    keywords='mental model, cognitative model, nlp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
)
