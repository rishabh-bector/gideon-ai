from setuptools import setup, find_packages
import os
setup(
    name="gideonai",
    version="0.0.1",
    author="Rishabh Bector and Leo Orshansky",
    author_email="bector.rishabh@gmail.com",
    description=("An intelligent bot written in Python"),
    license="BSD",
    keywords="gideon apiai bot intelligent",
    packages=find_packages(),
    install_requires=['gtts', 'wikipedia', 'pygame',
                      'apiai', 'speechrecognition', 'quizlet-api', 'pyjokes'],
)
