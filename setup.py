# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md') as f:
    readme_file = f.read()

# with open('LICENSE') as f:
#     license_file = f.read()

setup(
    name='gmusicripper',
    version='1.0.0',
    description='A Python package meant for automating MP3 ripping from Google Play Music',
    long_description=readme_file,
    author='docgloucester',
    url='https://github.com/docgloucester/Google-Play-Music-Ripper',
    # license=license_file
)