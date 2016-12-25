from setuptools import setup
import os
version = input("Version: ")
setup(
    name="gideonai",
    version=version,
    author="Rishabh Bector and Leo Orshansky",
    author_email="bector.rishabh@gmail.com",
    description=("An intelligent bot written in Python"),
    license="BSD",
    keywords="gideon apiai bot intelligent",
    packages=["gideonai"],
    entry_points={
        "console_scripts": ['gideonai = gideonai.__main__:main']
    },
    install_requires=['gtts', 'wikipedia', 'pygame',
                      'apiai', 'speechrecognition', 'quizlet', 'pyjokes', 'bs4', 'pafy', 'lxml', 'youtube-dl', 'pydub'],
    dependency_links=['https://github.com/s-alexey/quizlet/tarball#egg=quizlet-6.9']
)
